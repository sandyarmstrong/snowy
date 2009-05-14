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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from piston.handler import AnonymousBaseHandler
from piston.utils import rc

from snowy.notes.models import Note

class UserHandler(AnonymousBaseHandler):
    allow_methods = ('GET',)
    model = User

    def read(self, request, username):
        # TODO: abstract this out
        try:
            user = User.objects.get(username=username)
        except:
            return rc.NOT_HERE
        
        return {
            'first name': user.first_name,
            'last name': user.last_name,
            'notes-ref': reverse('note_index', kwargs={'username': username}),
            #'notes-api-ref': reverse('note_api_index', kwargs={'username': username}),
        }
