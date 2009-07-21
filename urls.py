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

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *

from snowy.users.forms import RegistrationFormUniqueUser
from snowy.notes.models import Note

from registration.views import activate
from registration.views import register

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'},
        name='snowy_index'),

    (r'^(?P<username>\w+)/notes/', include('snowy.notes.urls')),

    (r'^api/', include('snowy.api.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# Registration URLs
urlpatterns += patterns('',
    url(r'^registration/activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
    url(r'^registration/login/$', auth_views.login, {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^registration/logout/$', auth_views.logout, {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^registration/password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^registration/password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^registration/password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^registration/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^registration/password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^registration/password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^registration/register/$', register, {'form_class': RegistrationFormUniqueUser},
        name='registration_register'),
    url(r'^registration/register/complete/$', direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }))

# OAuth
urlpatterns += patterns('piston.authentication',
    url(r'^oauth/request_token/$', 'oauth_request_token'),
    url(r'^oauth/authenticate/$', 'oauth_user_auth'),
    url(r'^oauth/access_token/$', 'oauth_access_token'),
)

