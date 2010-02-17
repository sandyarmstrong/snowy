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
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Max

from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc, HttpStatusCode

from datetime import datetime
from dateutil import parser

from snowy.core.urlresolvers import reverse_full
from snowy.notes.models import Note
from snowy.notes.models import NoteTag
from snowy import settings

import pytz

# Use simplejson or Python 2.6 json, prefer simplejson.
try:
    import simplejson as json
except ImportError:
    import json

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

# http://domain/api/1.0
class RootHandlerAnonymous(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        kwargs = {'username': request.user.username}
        return basic_root()

# http://domain/api/1.0
class RootHandler(BaseHandler):
    allowed_methods = ('GET',)
    anonymous = RootHandlerAnonymous

    def read(self, request):
        kwargs = {'username': request.user.username}
        root = basic_root()
        root['user-ref'] = {
                'api-ref' : reverse_full('user_api_index', kwargs=kwargs),
                'href' : reverse_full('user_index', kwargs=kwargs),
            }
        return root

def basic_root():
    return {
        'oauth_request_token_url': reverse_full('oauth_request_token'),
        'oauth_authorize_url': reverse_full('oauth_user_auth'),
        'oauth_access_token_url': reverse_full('oauth_access_token'),
        'api-version': '1.0'
    }

# http://domain/api/1.0/user
class UserHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username):
        user = User.objects.get(username=username)
        profile = user.get_profile()
        kwargs = {'username': username}
        return {
            'user-name': user.username,
            'first-name': user.first_name,
            'last-name': user.last_name,
            'notes-ref': {
                'api-ref': reverse_full('note_api_index', kwargs=kwargs),
                'href': reverse_full('note_index', kwargs=kwargs),
            },
            'latest-sync-revision' : profile.latest_sync_rev,
            'current-sync-guid' : profile.current_sync_uuid
            # TODO: friends
        }

# http://domain/api/1.0/user/notes
class NotesHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT')

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username):
        author = User.objects.get(username=username)
        notes = Note.objects.user_viewable(request.user, author)

        if request.GET.has_key('since'):
            notes = notes.filter(last_sync_rev__gt=int(request.GET['since']))

        response = {'latest-sync-revision': author.get_profile().latest_sync_rev}
        if request.GET.has_key('include_notes'):
            response['notes'] = [describe_note(n) for n in notes]
        else:
            response['notes'] = [simple_describe_note(n) for n in notes]
        return response

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    @catch_and_return(KeyError, rc.BAD_REQUEST)
    @transaction.commit_on_success
    def update(self, request, username):
        def clean_date(date):
            return parser.parse(date).astimezone(pytz.utc)

        author = User.objects.get(username=username)
        if request.user != author:
            return rc.FORBIDDEN

        update = json.loads(request.raw_post_data)
        changes = update['note-changes']

        current_sync_rev = author.get_profile().latest_sync_rev
        new_sync_rev = current_sync_rev + 1

        if update.has_key('latest-sync-revision'):
            new_sync_rev = update['latest-sync-revision']

        if new_sync_rev != current_sync_rev + 1:
            # TODO: Return a more useful error response?
            return rc.BAD_REQUEST

        for c in changes:
            note, created = Note.objects.get_or_create(author=author,
                                                       guid=c['guid'])

            if c.has_key('command') and c['command'] == 'delete':
                note.delete()
                continue

            if c.has_key('title'): note.title = c['title']
            if c.has_key('note-content'): note.content = c['note-content']
            if c.has_key('note-content-version'): note.content_version = c['note-content-version']
            if c.has_key('last-change-date'): note.user_modified = clean_date(c['last-change-date'])
            if c.has_key('last-metadata-change-date'):
                note.modified = clean_date(c['last-metadata-change-date'])
            else:
                note.modified = datetime.now()
            if c.has_key('create-date'): note.created = clean_date(c['create-date'])
            if c.has_key('open-on-startup'): note.open_on_startup = (c['open-on-startup'] == True)
            if c.has_key('pinned'): note.pinned = (c['pinned'] == True)
            if c.has_key('tags'):
                note.tags.clear()
                for tag_name in c['tags']:
                    tag, created = NoteTag.objects.get_or_create(author=author,
                                                                 name=tag_name)
                    note.tags.add(tag)

            note.last_sync_rev = new_sync_rev
            note.save()

        profile = author.get_profile()
        if len(changes) > 0:
            profile.latest_sync_rev = new_sync_rev
            profile.save()
        
        return {
            'latest-sync-revision': profile.latest_sync_rev,
            'notes': [simple_describe_note(n) for n in Note.objects.filter(author=author)]
        }


# http://domain/api/1.0/user/notes/id
class NoteHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Note

    @catch_and_return(ObjectDoesNotExist, rc.NOT_HERE)
    def read(self, request, username, note_id):
        author = User.objects.get(username=username)
        note = Note.objects.get(pk=note_id, author=author)
        if request.user != author and note.permissions == 0:
            return rc.FORBIDDEN
        return {'note': [describe_note(note)]}

def describe_note(note):
    def local_iso(date):
        return date.replace(tzinfo=pytz.utc).isoformat()
        #TODO: Return new format below for newer clients
        #return date.replace(tzinfo=pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    return {
        'guid': note.guid,
        'title': note.title,
        'note-content': note.content,
        'last-change-date': local_iso(note.user_modified),
        'last-metadata-change-date': local_iso(note.modified),
        'create-date': local_iso(note.created),
        'open-on-startup': note.open_on_startup,
        'pinned': note.pinned,
        'last-sync-revision': note.last_sync_rev,
        'tags': [t.name for t in note.tags.all()],
    }

def simple_describe_note(note):
    kwargs = {'username': note.author.username, 'note_id': note.pk}
    return {
        'guid': note.guid,
        'ref': {
            'api-ref': reverse_full('note_api_detail', kwargs=kwargs),
            'href': reverse_full('note_detail_no_slug', kwargs=kwargs),
        },
        'title': note.title
    }
