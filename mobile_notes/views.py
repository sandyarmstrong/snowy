#
# Copyright (c) 2010 Sandy Armstrong <sanfordarmstrong@gmail.com>
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

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response

from django.template import RequestContext

from snowy.core.urlresolvers import reverse_full

from settings import MEDIA_URL

def mobile_note_index_redirect(request):
    return HttpResponseRedirect(reverse_full('mobile_note_index'))

def mobile_note_js(request):
    return render_to_response('mobile/slicknotes.js',
                              {'root_uri': reverse_full('api_root'),
                               'note_xml_to_html_xsl_uri': MEDIA_URL + 'xsl/note2xhtml.xsl',
                               },
                              context_instance=RequestContext(request))

def mobile_note_index(request):
    return render_to_response('mobile/index.html',
                              {'jquery_uri': MEDIA_URL + 'js/jquery.min.js',
                               'jquery_mobile_js_uri': MEDIA_URL + 'js/jquery.mobile-1.0a2.js',
                               'jquery_mobile_css_uri': MEDIA_URL  + 'css/jquery.mobile-1.0a2.min.css',
                              },
                              context_instance=RequestContext(request))

def cache_manifest(request):
    return render_to_response('mobile/cache.manifest',
                              {'root_uri': reverse_full('api_root'),
                               'jquery_uri': MEDIA_URL + 'js/jquery.min.js',
                               'jquery_mobile_js_uri': MEDIA_URL + 'js/jquery.mobile-1.0a2.js',
                               'jquery_mobile_css_uri': MEDIA_URL  + 'css/jquery.mobile-1.0a2.min.css',
                               'note_xml_to_html_xsl_uri': MEDIA_URL + 'xsl/note2xhtml.xsl',
                              },
                              mimetype='text/cache-manifest',
                              context_instance=RequestContext(request))
