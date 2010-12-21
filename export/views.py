#
# Copyright (c) 2010 Tony Young <rofflwaffls@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from snowy.api.handlers import describe_note
from snowy.notes.models import Note

import tarfile

import time
from dateutil.parser import parse as parse_iso_time

from xml.dom.minidom import Document, parseString

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

# list of allowed fields
ALLOWED_FIELDS = [ "title", "note-content", "last-change-date", "last-metadata-change-date", "create-date", "tags", "open-on-startup" ]

def _get_data(request):
    notes = Note.objects.user_viewable(request.user, User.objects.get(username=request.user))
    return [describe_note(n) for n in notes]

def _note_to_xml(doc, note):
    root = doc.createElement("note")
    root.setAttribute("xmlns", "http://beatniksoftware.com/tomboy")
    root.setAttribute("xmlns:link", "http://beatniksoftware.com/tomboy/link")
    root.setAttribute("xmlns:size", "http://beatniksoftware.com/tomboy/size")
    root.setAttribute("version", "0.3")

    for field in ALLOWED_FIELDS:
        if field == "note-content":
            wrap_elem = doc.createElement("text")
            wrap_elem.setAttribute("xml:space", "preserve")

            # make expat parse nicely
            subdoc = parseString('<note-content xmlns:link="urn:tempuri" xmlns:size="urn:tempuri">%s\n\n%s</note-content>' % (
                note["title"].encode("utf-8"),
                note[field].encode("utf-8")
            ))

            elem = subdoc.documentElement

            # quietly get rid of temporary namespaces
            elem.removeAttribute("xmlns:link")
            elem.removeAttribute("xmlns:size")
            
            elem.setAttribute("version", "0.1")

            wrap_elem.appendChild(elem)
            elem = wrap_elem
        else:
            elem = doc.createElement(field)

            if field == "tags":
                for tag in note[field]:
                    tag_elem = doc.createElement("tag")
                    tag_elem.appendChild(doc.createTextNode(tag))
                    elem.appendChild(tag_elem)
            else:
                content = note[field]
                if not isinstance(content, unicode):
                    content = str(content)
                elem.appendChild(doc.createTextNode(content))

        root.appendChild(elem)

    return root

@login_required
def export_tar(request):
    data = _get_data(request)

    arch_file = StringIO()
    arch = tarfile.TarFile(fileobj=arch_file, mode="w")

    for note in data:
        doc = Document()
        root = _note_to_xml(doc, note)
        doc.appendChild(root)

        note_data = doc.toxml(encoding='utf-8')

        note_file = StringIO()
        note_file.write(note_data)
        note_file.seek(0)

        note_info = tarfile.TarInfo("%s.note" % note["guid"])
        note_info.size = len(note_data)
        note_info.mtime = time.mktime(parse_iso_time(note["last-change-date"]).timetuple())

        arch.addfile(
            tarinfo=note_info,
            fileobj=note_file
        )

    arch.close()

    response = HttpResponse(arch_file.getvalue())
    response["Content-Type"] = "application/x-tar"
    response["Content-Disposition"] = "attachment; filename=snowy-%s-%s.tar" % (request.user, time.strftime("%Y-%m-%d"))
    return response
