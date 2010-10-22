# Copyright (c) 2009 Brad Taylor <brad@getcoded.net>
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
from snowy.notes.models import Note
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from snowy.notes.templates import CONTENT_TEMPLATES, DEFAULT_CONTENT_TEMPLATE

def note_to_html(note, author):
    """
    Convert a note into a html string
    """
    from lxml import etree
    import os.path

    # Extension function for XSL. Called twice per link,
    # so we keep a little cache to save on lookups
    link_cache = {}
    def get_url_for_title(dummy, link_text):
        if link_text in link_cache:
            return link_cache[link_text]
        try:
            note = Note.objects.get(author=author, title=link_text)
            note_url = note.get_absolute_url()
            link_cache[link_text] = note_url
            return note_url
        except ObjectDoesNotExist:
            return None

    ns = etree.FunctionNamespace("http://tomboy-online.org/stuff")
    ns.prefix = "tomboyonline"
    ns['get_url_for_title'] = get_url_for_title

    style = etree.parse(os.path.join(settings.PROJECT_ROOT,
                                     'data/note2xhtml.xsl'))
    transform = etree.XSLT(style)

    template = CONTENT_TEMPLATES.get(note.content_version, DEFAULT_CONTENT_TEMPLATE)
    complete_xml = template.replace('%%%CONTENT%%%', note.content)
    doc = etree.fromstring(complete_xml)

    result = transform(doc)
    body = str(result)
    return body
