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

from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from piston.resource import Resource

from snowy.api.handlers import *

auth = HttpBasicAuthentication(realm='Snowy')
authoauth = OAuthAuthentication(realm='Snowy')
ad = {'authentication': authoauth}

""" piston resources are marked csrf_exempt to ensure the the django
CsrfMiddleware doesn't interfere with POST requests
http://bitbucket.org/jespern/django-piston/issue/82/post-requests-fail-when-using-django-trunk """

root_handler = Resource(handler=RootHandler, **ad)
root_handler.csrf_exempt = getattr(root_handler.handler, 'csrf_exempt', True)
user_handler = Resource(UserHandler)
user_handler.csrf_exempt = getattr(user_handler.handler, 'csrf_exempt', True)
notes_handler = Resource(handler=NotesHandler, **ad)
notes_handler.csrf_exempt = getattr(notes_handler.handler, 'csrf_exempt', True)
note_handler = Resource(handler=NoteHandler, **ad)
note_handler.csrf_exempt = getattr(note_handler.handler, 'csrf_exempt', True)

urlpatterns = patterns('',
    # 1.0 API methods
    url(r'1.0/(?P<username>\w+)/notes/(?P<note_id>\d+)/$', note_handler, name='note_api_detail'),
    url(r'1.0/(?P<username>\w+)/notes/$', notes_handler, name='note_api_index'),
    url(r'1.0/(?P<username>\w+)/$', user_handler, name='user_api_index'),
    url(r'1.0/$', root_handler),
)
