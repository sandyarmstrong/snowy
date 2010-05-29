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

from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from recaptcha_django import ReCaptchaField
from django.conf import settings
from django import forms

class RegistrationFormUniqueUser(RegistrationFormUniqueEmail):
    """
    Subclass of ``RegistrationFormUniqueEmail`` which verifies usernames
    against a blacklist.
    """
    captcha = ReCaptchaField(label=_(u'Verify words'))

    username_blacklist = ['about', 'accounts', 'admin', 'api', 'blog',
                          'contact', 'css', 'friends', 'images', 'index.html',
                          'news', 'notes', 'oauth', 'pony', 'register',
                          'registration', 'site_media', 'snowy', 'tomboy']

    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueUser, self).__init__(*args, **kwargs)

        #print self.fields['captcha'].widget.html
        if not settings.RECAPTCHA_ENABLED:
            del self.fields['captcha']
        
        self.fields['username'].label = _(u'Username')
        self.fields['username'].help_text = _(u'Maximum of 30 characters in length.')

        self.fields['email'].label = _(u'Email address')

        self.fields['password1'].label = _(u'Choose a password')
        self.fields['password1'].help_text = _(u'Minimum of 6 characters in length.')

        self.fields['password2'].label = _(u'Re-enter password')

    def clean_username(self):
        """
        Validate that the user doesn't exist in our blacklist.
        """
        username = self.cleaned_data['username']
        if username in self.username_blacklist:
            raise forms.ValidationError(_(u'This username has been reserved.  Please choose another.'))
        return username

    def clean_password1(self):
        """
        Validate that the password is at least 6 characters long.
        """
        password = self.cleaned_data['password1']
        if len(password) < 6:
            raise forms.ValidationError(_(u'Your password must be at least 6 characters long.'))

        return password

class OpenIDRegistrationFormUniqueUser(RegistrationFormUniqueUser):
    def __init__(self, *args, **kwargs):
        super(OpenIDRegistrationFormUniqueUser, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

from snowy.accounts.models import UserProfile

class InternationalizationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('language', )

class DisplayNameChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name',)

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
