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

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.template import RequestContext
from django.conf import settings

from snowy.accounts.models import UserProfile
from snowy.accounts.forms import InternationalizationForm, OpenIDRegistrationFormUniqueUser

def openid_registration(request, template_name='registration/registration_form.html'):
    try:
        openid_response = request.session['openid_response']
        # do sreg magic here
    except KeyError:
        return HttpResponseNotAllowed(_(u'No openid_response object for this session!'))

    registration_form = OpenIDRegistrationFormUniqueUser(request.POST or None)

    if registration_form.is_valid():
        user = authenticate(openid_response=openid_response,
                            username=registration_form.cleaned_data.get('username', ''),
                            create_user=True)
        # Clear the openid_response from the session so it can't be used to create another account
        del request.session['openid_response']

        if user is not None:
            email = registration_form.cleaned_data.get('email', '')
            if email:
                user.email = email

            display_name = registration_form.cleaned_data.get('display_name', '')
            if display_name:
                user.get_profile().display_name = display_name

            user.save()
            user.get_profile().save()
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                return HttpResponseNotAllowed(_(u'Disabled account'))
        else:
            return HttpResponseNotAllowed(_(u'Unknown user'))

    return render_to_response(template_name,
                              {'form' : registration_form},
                              context_instance=RequestContext(request))

@login_required
def accounts_preferences(request, template_name='accounts/preferences.html'):
    user = request.user
    profile = user.get_profile()

    if 'password_form' in request.POST:
        password_form = PasswordChangeForm(user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
    else:
        password_form = PasswordChangeForm(user)

    if 'email_form' in request.POST:
        email_form = EmailChangeForm(request.POST, instance=profile)
        if email_form.is_valid():
            print 'Email form is valid!'
            email_form.save()
    else:
        email_form = EmailChangeForm(instance=profile)

    if 'display_name_form' in request.POST:
        display_name_form = DisplayNameChangeForm(request.POST, instance=profile)
        if display_name_form.is_valid():
            print 'Display Name form is valid!'
            display_name_form.save()
    else:
        display_name_form = DisplayNameChangeForm(instance=profile)


    if 'i18n_form' in request.POST:
        i18n_form = InternationalizationForm(request.POST, instance=profile)
        if i18n_form.is_valid():
            print 'Internationalization form is valid!'
            i18n_form.save()
    else:
        i18n_form = InternationalizationForm(instance=profile)

    return render_to_response(template_name,
                              {'user': user, 'i18n_form': i18n_form,
                               'password_form': password_form,
                               'email_form' : email_form,
                               'display_name_form' : display_name_form},
                              context_instance=RequestContext(request))
