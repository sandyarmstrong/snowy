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
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    content_version = models.CharField(max_length=10)
    tags = models.ManyToManyField('NoteTag', null=True, blank=True)
    permissions = models.IntegerField(choices=NOTE_PERMISSIONS,
                                      default=0)

    def __unicode__(self):
        return self.title

class NoteTag(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    is_notebook = models.BooleanField()

    def __unicode__(self):
        return self.name
