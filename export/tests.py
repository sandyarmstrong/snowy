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

from django.test import TestCase

import snowy.export.views

import datetime
import re
import tarfile
from xml.dom.minidom import parseString, parse

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class fake_request(object):
    class user:
        @staticmethod
        def is_authenticated():
            return True

class ExportTest(TestCase):
    def setUp(self):
        # monkey patch snowy.export._get_data to return what we want
        self.data = [
            {
                "guid" : "00000000-0000-0000-0000-000000000000",
                "note-content": u"here is a note <bold>with random tags</bold>　ａｎｄ　ｕｎｉｃｏｄｅ",
                "open-on-startup": True,
                "last-metadata-change-date": "1970-01-01T13:00:00Z",
                "title": u"note 壱",
                "tags": [ u"herë", "are", "some", "tags" ],
                "create-date": "1970-01-01T13:00:00Z",
                "last-change-date": "1970-01-01T13:00:00Z"
            },
            {
                "guid" : "00000000-0000-0000-0000-000000000001",
                "note-content": u"here is another note with äçcèñts",
                "open-on-startup": False,
                "last-metadata-change-date": "1970-01-01T13:00:00Z",
                "title": u"ノート 2",
                "tags": [ "here", "are", "some", "tags", "too" ],
                "create-date": "1970-01-01T13:00:00Z",
                "last-change-date": "1970-01-01T13:00:00Z"
            }
        ]

        self.grouped_data = dict([
            (note["guid"], note) for note in self.data
        ])

        def _get_data(request):
            return self.data
        snowy.export.views._get_data = _get_data

    def _assert_xml(self, note_node, data):
        tag_wrap_expr = re.compile(r"\<.+?\>(.*)\</.+?\>", re.MULTILINE | re.DOTALL)

        guid = note_node.getAttribute("guid")
        for child_node in note_node.childNodes:
            tag = child_node.tagName

            content = child_node.toxml()
            content = tag_wrap_expr.match(content).group(1)

            if tag == "text":
                self.assertEquals(tag_wrap_expr.match(child_node.childNodes[0].toxml()).group(1), "%s\n\n%s" % (data["title"], data["note-content"]))
            elif tag == "tags":
                self.assertEquals([ tag.childNodes[0].toxml() for tag in child_node.childNodes ], data["tags"])
            elif tag == "open-on-startup":
                self.assertEquals(content == "True" and True or False, data[tag])
            else:
                self.assertEquals(content, data[tag])

    def test_tar_export(self):
        data = tarfile.TarFile(fileobj=StringIO(snowy.export.views.export_tar(fake_request).content), mode="r")
        for info in data:
            doc = parse(data.extractfile(info.name))
            self._assert_xml(doc.childNodes[0], self.grouped_data[info.name.split(".")[0]])
