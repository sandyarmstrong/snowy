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

import uuid

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.db import models

from autoslug.fields import AutoSlugField

class Note(models.Model):
    NOTE_PERMISSIONS = (
        (0, 'Private'), (1, 'Public'), 
    )

    guid = models.CharField(max_length=36)

    author = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.DateTimeField(auto_now_add=True)

    title = models.TextField(blank=True)
    slug = AutoSlugField(unique_with='author', populate_from='title',
                         editable=True)
    content = models.TextField(blank=True)
    content_version = models.CharField(max_length=10, blank=True)

    tags = models.ManyToManyField('NoteTag', null=True, blank=True)
    permissions = models.IntegerField(choices=NOTE_PERMISSIONS,
                                      default=0)

    open_on_startup = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    
    last_sync_rev = models.IntegerField(default=-1)

    class Meta:
        get_latest_by = 'user_modified'
        unique_together = (('author', 'title'), ('author', 'guid'), )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.slug == "":
            return ('note_detail_no_slug', (), {
                'note_id': self.id,
                'username': self.author.username,
            })
        else:
            return ('note_detail', (), {
                'note_id': self.id,
                'username': self.author.username,
                'slug': self.slug,
            })


class NoteTag(models.Model):
    author = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    is_notebook = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author', 'name')

    def __unicode__(self):
        return self.name

    def get_name_for_display(self):
        if self.is_notebook:
            return self.name.split(':', 2)[-1]
        return self.name

def _update_is_notebook(sender, instance, **kwargs):
    """
    Update is_notebook based upon the NoteTag name.
    """
    instance.is_notebook = instance.name.startswith('system:notebook:')

pre_save.connect(_update_is_notebook, sender=NoteTag,
                 dispatch_uid='snowy.notes.models.NoteTag')


class UserProfile(models.Model):
    def _create_uuid():
        return str(uuid.uuid4())

    user = models.ForeignKey(User, unique=True)
    latest_sync_rev = models.IntegerField(default=-1)
    current_sync_uuid = models.CharField(max_length=36, default=_create_uuid)

def _create_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile object in response to a new User being created.
    """
    if not created: return
    UserProfile.objects.create(user=instance)

post_save.connect(_create_profile, sender=User,
                  dispatch_uid='django.contrib.auth.models.User')
