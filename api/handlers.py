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

class catch_and_return(object):
    def __init__(self, err, response):
        self.err = err
        self.response = response

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except self.err:
                return self.response
        return wrapper

class UserHandler(AnonymousBaseHandler):
    allow_methods = ('GET',)

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username):
        user = User.objects.get(username=username)
        reverse_args = {'username': username}
        return {
            'first-name': user.first_name,
            'last-name': user.last_name,
            'notes-ref': {
                'api-ref': reverse('note_api_index', kwargs=reverse_args),
                'href': reverse('note_index', kwargs=reverse_args),
            },
        }

class ListNoteRefsHandler(BaseHandler):
    allow_methods = ('GET',)

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username):
        user = User.objects.get(username=username)
        if request.GET.has_key('include_notes'):
            return {'notes': [describe_note(n) for n in Note.objects.filter(author=user)] }
        else:
            return {'note-refs': [{
                    'guid': n.guid,
                    'ref': {
                        'api-ref': reverse('note_api_detail', kwargs={
                            'username': n.author.username,
                            'note_id': n.pk,
                            'slug': n.slug,
                        }),
                        'href': n.get_absolute_url(),
                    },
                    'title': n.title,
                }
                for n in Note.objects.filter(author=user)
            ]}

class NoteHandler(BaseHandler):
    allow_methods = ('GET',)
    model = Note

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username, note_id, slug):
        user = User.objects.get(username=username)
        note = Note.objects.get(pk=note_id, slug=slug)
        return {'note': [describe_note(note)]}


def describe_note(note):
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
