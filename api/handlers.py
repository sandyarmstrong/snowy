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

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, HttpStatusCode

from snowy.notes.models import Note

def get_user_or_not_here(username):
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise HttpStatusCode('Gone', code=410)

def get_note_or_not_here(note_id):
    try:
        return Note.objects.get(pk=note_id)
    except ObjectDoesNotExist:
        raise HttpStatusCode('Gone', code=410)

class UserHandler(AnonymousBaseHandler):
    allow_methods = ('GET',)

    def read(self, request, username):
        user = get_user_or_not_here(username)
        return {
            'first name': user.first_name,
            'last name': user.last_name,
            'notes-ref': reverse('note_index', kwargs={'username': username}),
            'notes-api-ref': reverse('note_api_index', kwargs={'username': username}),
        }

class ListNoteRefsHandler(BaseHandler):
    allow_methods = ('GET',)

    def read(self, request, username):
        user = get_user_or_not_here(username)
        return {'note-refs': [
            {'guid': n.guid, 'href': n.get_absolute_url(), 'title': n.title }
            for n in Note.objects.filter(author=user)
        ]}

class NoteHandler(BaseHandler):
    allow_methods = ('GET',)
    model = Note

    def read(self, request, username, note_id, slug=None):
        user = get_user_or_not_here(username)
        note = get_note_or_not_here(note_id)
        return {
            'guid': note.guid,
            'title': note.title,
            'note-content': note.content,
            'last-change-date': note.user_modified,
            'last-metadata-change-date': note.modified,
            'create-date': note.created,
            'open-on-startup': note.open_on_startup,
            'tags': [t.name for t in note.tags.all()],
        }
