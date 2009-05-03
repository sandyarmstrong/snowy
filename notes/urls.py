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
from django.views.generic.list_detail import object_list, object_detail
from snowy.notes.models import Note

notes_dict = {'queryset': Note.objects.all(), }

urlpatterns = patterns('',
    (r'^$', object_list, notes_dict),
    url(r'^(?P<note_id>\d+)/$', 'snowy.notes.views.note_detail', name='note_detail'),
)
