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

from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from snowy.notes.templates import CONTENT_TEMPLATES, DEFAULT_CONTENT_TEMPLATE
from snowy.notes.models import *
from snowy import settings

from piston import forms as piston_forms

def note_index(request, username,
               template_name='note/note_index.html'):
    author = get_object_or_404(User, username=username)

    # TODO: retrieve the last open note from the user
    last_modified = Note.objects.user_viewable(request.user, author) \
                                .order_by('-user_modified')
    if last_modified.count() > 0:
        return HttpResponseRedirect(last_modified[0].get_absolute_url())
    
    # TODO: Instruction page to tell user to either sync or create a new note
    return render_to_response(template_name,
                              {'author': author},
                              context_instance=RequestContext(request))

def note_detail(request, username, note_id, slug='',
                template_name='notes/note_detail.html'):
    author = get_object_or_404(User, username=username)
    note = get_object_or_404(Note, pk=note_id, author=author)

    if request.user != author and note.permissions == 0:
        return HttpResponseForbidden()
        
    if note.slug != slug:
        return HttpResponseRedirect(note.get_absolute_url())
    
    # break this out into a function
    import libxslt
    import libxml2
    
    style, doc, result = None, None, None
 
    try:
        styledoc = libxml2.parseFile('data/note2xhtml.xsl')
        style = libxslt.parseStylesheetDoc(styledoc)
    
        template = CONTENT_TEMPLATES.get(note.content_version, DEFAULT_CONTENT_TEMPLATE)
        doc = libxml2.parseDoc(template.replace('%%%CONTENT%%%', note.content.encode('UTF-8')))
        result = style.applyStylesheet(doc, None)

        # libxml2 doesn't munge encodings, so forcibly decode from UTF-8
        body = unicode(style.saveResultToString(result), 'UTF-8')
    finally:
        if style != None: style.freeStylesheet()
        if doc != None: doc.freeDoc()
        if result != None: result.freeDoc()

    return render_to_response(template_name,
                              {'title': note.title,
                               'note': note, 'body': body,
                               'request': request, 'author': author},
                              context_instance=RequestContext(request))
