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

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings

from snowy.accounts.forms import InternationalizationForm

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

    if 'i18n_form' in request.POST:
        i18n_form = InternationalizationForm(request.POST, instance=profile)
        if i18n_form.is_valid():
            print 'Internationalization form is valid!'
            i18n_form.save()
    else:
        i18n_form = InternationalizationForm(instance=profile)

    return render_to_response(template_name,
                              {'user': user, 'i18n_form': i18n_form,
                               'password_form': password_form},
                              context_instance=RequestContext(request))
