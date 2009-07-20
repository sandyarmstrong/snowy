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

from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django import forms

class RegistrationFormUniqueUser(RegistrationFormUniqueEmail):
    """
    Subclass of ``RegistrationFormUniqueEmail`` which verifies usernames
    against a blacklist.
    """
    username_blacklist = ['about', 'accounts', 'admin', 'api', 'blog',
                          'contact', 'css', 'friends', 'images', 'index.html',
                          'news', 'notes', 'oauth', 'pony', 'register',
                          'registration', 'site_media', 'snowy', 'tomboy' ]

    def clean_username(self):
        """
        Validate that the user doesn't exist in our blacklist.
        """
        username = self.cleaned_data['username']
        if username in self.username_blacklist:
            raise forms.ValidationError(_(u'This username has been reserved.  Please choose another.'))
        return username
