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
from snowy.notes.models import Note

urlpatterns = patterns('',
    url(r'^$', 'snowy.notes.views.note_index', name='note_index'),
    url(r'^list/$', 'snowy.notes.views.note_list', name='note_list'),
    url(r'^(?P<note_id>\d+)/$', 'snowy.notes.views.note_detail', name='note_detail_no_slug'),
    url(r'^(?P<note_id>\d+)/(?P<slug>[^/]+)/$', 'snowy.notes.views.note_detail', name='note_detail'),
)
