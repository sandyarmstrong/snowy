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

from django.conf.urls.defaults import *

from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from snowy.api.handlers import *

auth = HttpBasicAuthentication(realm='Snowy')
ad = {'authentication': auth}

user_handler = Resource(UserHandler)
notes_handler = Resource(handler=NotesHandler, **ad)
note_handler = Resource(handler=NoteHandler, **ad)

urlpatterns = patterns('',
    # 1.0 API methods
    url(r'1.0/(?P<username>\w+)/notes/(?P<note_id>\d+)/$', note_handler, name='note_api_detail'),
    url(r'1.0/(?P<username>\w+)/notes/$', notes_handler, name='note_api_index'),
    url(r'1.0/(?P<username>\w+)/$', user_handler),
)
