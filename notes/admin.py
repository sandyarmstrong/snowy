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

from snowy.accounts.models import UserProfile
from snowy.notes.models import Note, NoteTag
from reversion.admin import VersionAdmin
from django.contrib import admin

class NoteAdmin(VersionAdmin):
    list_display = ('created', 'author', 'title')
    search_fields = ['content', 'title']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Note, NoteAdmin)
admin.site.register(NoteTag)
admin.site.register(UserProfile)
