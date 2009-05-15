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

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    NOTE_PERMISSIONS = (
        (0, 'Private'), (1, 'Public'), 
    )

    guid = models.CharField(max_length=36)

    author = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=128, blank=True)
    slug = models.SlugField(blank=True)
    content = models.TextField(blank=True)
    content_version = models.CharField(max_length=10, blank=True)

    tags = models.ManyToManyField('NoteTag', null=True, blank=True)
    permissions = models.IntegerField(choices=NOTE_PERMISSIONS,
                                      default=0)

    open_on_startup = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'user_modified'
        unique_together = (('author', 'title'), ('author', 'guid'), )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
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


class VersionMetadata(models.Model):
    revision = models.ForeignKey('reversion.Revision')
    version = models.IntegerField()
