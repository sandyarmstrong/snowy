#
# Copyright (c) 2009 Brad Taylor <brad@getcoded.net>
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions: 
#  
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software. 
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
#

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from snowy.notes.models import *

def note_detail(request, note_id,
                template_name='notes/note_detail.html'):
    note = get_object_or_404(Note, pk=note_id)
    
    # break this out into a function
    import libxslt
    import libxml2
    
    style, doc, result = None, None, None
 
    try:
        styledoc = libxml2.parseFile('data/note2xhtml.xsl')
        style = libxslt.parseStylesheetDoc(styledoc)
    
        doc = libxml2.parseDoc(note.body)
        result = style.applyStylesheet(doc, None)
    
        body = style.saveResultToString(result)
    finally:
        if style != None: style.freeStylesheet()
        if doc != None: doc.freeDoc()
        if result != None: result.freeDoc()

    return render_to_response(template_name,
                              {'note': note, 'body': body },
                              context_instance=RequestContext(request))
