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

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

import uuid

class UserProfile(models.Model):
    def _create_uuid():
        return str(uuid.uuid4())

    user = models.ForeignKey(User, unique=True)
    latest_sync_rev = models.IntegerField(default=-1)
    current_sync_uuid = models.CharField(max_length=36, default=_create_uuid)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                verbose_name=_(u'Application Language'),
                                null=True, blank=True)
    display_name = models.CharField(_('display name'), max_length=80)
    openid_user = models.BooleanField(verbose_name=_(u'OpenID User'),)

    def __unicode__(self):
        return str(self.user)

def _create_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile object in response to a new User being created.
    """
    if not created: return
    UserProfile.objects.create(user=instance)

post_save.connect(_create_profile, sender=User,
                  dispatch_uid='django.contrib.auth.models.User')
