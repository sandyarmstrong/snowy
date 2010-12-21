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

from snowy.accounts.forms import RegistrationFormUniqueUser

from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *

from registration.views import activate
from registration.views import register

import snowy.accounts.views
import django_openid_auth.views

import snowy.export.views

urlpatterns = patterns('',
    url(r'^preferences/$', 'snowy.accounts.views.accounts_preferences',
        name='preferences'),

    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'},
        name='auth_logout'),

    # OpenID URLs
    # names must not be altered because django_openid_auth has to reverse them
    url(r'^openid/login/$', snowy.accounts.views.openid_begin,
        {'template_name': 'openid/login.html'}, name='openid-login'),
    url(r'^openid/complete/$', snowy.accounts.views.openid_complete,
        name='openid-complete'),
    url(r'^openid/registration/$', snowy.accounts.views.openid_registration,
        name='openid_registration'),

    # Registration URLs
    url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
    url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^register/login/$', auth_views.login, {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^register/$', register, {'form_class': RegistrationFormUniqueUser},
        name='registration_register'),
    url(r'^register/complete/$', direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)
