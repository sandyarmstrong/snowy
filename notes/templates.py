#
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

# libxml2 doesn't munge encodings, so forcibly encode items to UTF-8
# http://mail.gnome.org/archives/xml/2004-February/msg00363.html
CONTENT_TEMPLATES = {
    '0.1': """
<note-content version="0.1" 
 xmlns:link="http://beatniksoftware.com/tomboy/link"
 xmlns:size="http://beatniksoftware.com/tomboy/size"
 xmlns="http://beatniksoftware.com/tomboy">
 %%%CONTENT%%%
</note-content>""".encode('UTF-8'),
}

DEFAULT_CONTENT_TEMPLATE = CONTENT_TEMPLATES['0.1']
