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

def validate_username_blacklist(username):
    """
    Verifies that the username is not on the blacklist of reserved usernames
    """
    print "Validate"
    username_blacklist = ['about', 'accounts', 'admin', 'api', 'blog',
                          'contact', 'css', 'friends', 'images', 'index.html',
                          'news', 'notes', 'oauth', 'pony', 'register',
                          'registration', 'site_media', 'snowy', 'tomboy']
    if username in username_blacklist:
        raise forms.ValidationError(_(u'This username has been reserved.  Please choose another.'))

class RegistrationFormUniqueUser(RegistrationFormUniqueEmail):
    """
    Subclass of ``RegistrationFormUniqueEmail`` which verifies usernames
    against a blacklist and adds a captcha.
    """
    captcha = ReCaptchaField(label=_(u'Verify words:'))

    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueUser, self).__init__(*args, **kwargs)

        if not settings.RECAPTCHA_ENABLED:
            del self.fields['captcha']
        
        self.fields['username'].label = _(u'Username:')
        self.fields['username'].help_text = _(u'Maximum of 30 characters in length.')
        self.fields['username'].validators = [validate_username_blacklist,
                                              validate_username_available]

        self.fields['email'].label = _(u'Email address:')

        self.fields['password1'].label = _(u'Choose a password:')
        self.fields['password1'].help_text = _(u'Minimum of 6 characters in length.')

        self.fields['password2'].label = _(u'Re-enter password:')

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_username_blacklist(username)
        return username

    def clean_password1(self):
        """
        Validate that the password is at least 6 characters long.
        """
        password = self.cleaned_data['password1']
        if len(password) < 6:
            raise forms.ValidationError(_(u'Your password must be at least 6 characters long.'))

        return password

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

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_username_blacklist(username)
        return username


