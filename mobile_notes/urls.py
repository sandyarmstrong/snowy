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

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'snowy.mobile_notes.views.mobile_note_index_redirect'),
    url(r'index.html$', 'snowy.mobile_notes.views.mobile_note_index', name='mobile_note_index'),
    url(r'cache.manifest$', 'snowy.mobile_notes.views.cache_manifest', name='cache_manifest'),
    url(r'slicknotes.js$', 'snowy.mobile_notes.views.mobile_note_js', name='mobile_note_js'), # TODO: Static instead?
)
