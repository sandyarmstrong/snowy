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

from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q

from snowy.notes.utils  import note_to_html
from snowy.notes.models import *

def note_index(request, username,
               template_name='notes/note_index.html'):
    author = get_object_or_404(User, username=username)
    enabled = author.is_active

    # TODO: retrieve the last open note from the user
    last_modified = Note.objects.user_viewable(request.user, author) \
                                .order_by('-user_modified')
    if last_modified.count() > 0:
        return HttpResponseRedirect(last_modified[0].get_absolute_url())

    # TODO: Instruction page to tell user to either sync or create a new note
    return render_to_response(template_name,
                              {'author': author,
                               'enabled': enabled,
                               # Django 1.1 does not support == operator, so
                               # we need to do the check here and pass it along
                               'author_is_user': username==request.user.username},
                              context_instance=RequestContext(request))

def note_list(request, username,
              template_name='notes/note_list.html'):
    author = get_object_or_404(User, username=username)
    notes = Note.objects.user_viewable(request.user, author)
    return render_to_response(template_name,
                              {'notes': notes},
                              context_instance=RequestContext(request))

def note_detail(request, username, note_id, slug='',
                template_name='notes/note_detail.html'):
    author = get_object_or_404(User, username=username)
    note = get_object_or_404(Note, pk=note_id, author=author)

    if request.user != author and note.permissions == 0:
        return HttpResponseForbidden()

    if note.slug != slug:
        return HttpResponseRedirect(note.get_absolute_url())

    body = note_to_html(note, author)

    try:
        # Get the notebook name, if any
        notebook = note.tags.get(is_notebook=True)
        if notebook:
            notebook = notebook.get_name_for_display()
    except ObjectDoesNotExist:
        notebook = []

    return render_to_response(template_name,
                              {'title': note.title,  'note': note,
                               'notebook': notebook, 'body': body,
                               'request': request, 'author': author},
                              context_instance=RequestContext(request))
