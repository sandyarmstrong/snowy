#
# Copyright (c) 2010 Jeff Schroeder <jeffschroeder@computer.org>
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

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class ExtendedUserAdmin(UserAdmin):
    """Simplify mass user moderation"""

    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_editable = ('is_active',)
    actions = ('batch_user_enable', 'batch_user_disable',)

    def _batch_user_modify(self, request, queryset, enable):
        rows_updated = queryset.update(is_active=enable)
        if rows_updated == 1:
            msg = "1 user was"
        else:
            msg = "%s users were" % rows_updated
        if enable:
            action = "enabled"
        else:
            action = "disabled"
        # Django's built-in messaging requires basestring-like objects in 1.1
        self.message_user(request, unicode(_("%s successfully %s" % (msg, action))))

    def batch_user_enable(self, request, queryset):
        self._batch_user_modify(request, queryset, enable=True)

    def batch_user_disable(self, request, queryset):
        self._batch_user_modify(request, queryset, enable=False)

    batch_user_enable.short_description  = _("Enable selected users")
    batch_user_disable.short_description = _("Disable selected users")

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
