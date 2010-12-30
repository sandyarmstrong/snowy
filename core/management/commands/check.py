# Copyright (c) 2010 Jeff Schroeder <jeffschroeder@computer.org>
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

from django.conf import settings
from django.db.models import get_models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.management.color import color_style
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext_lazy as _

class Command(NoArgsCommand):
    """
    Check that snowy is properly set up
    """
    def __init__(self):
        self.errors = []
        self.messages = []
        self.style = color_style()

    def error(self, string):
        return self.style.ERROR(string)

    def notice(self, string):
        return self.style.HTTP_REDIRECT(string)

    def handle_noargs(self, **options):
        """
        When called as: manage.py check
        """
        self.run_db_check()
        self.run_site_check()

        if self.messages:
            print self.notice(_("Completed Successfully:"))
            for message in self.messages:
                print "\t%s" % message
            print ""

        if self.errors:
            print self.error(_("Completed with errors:"))

            for error in self.errors:
                print "\t%s" % error

    def run_db_check(self):
        try:
            for model in get_models():
                # The fastest query I could think of. Also, since queries are
                # ran lazily, casting the qs to a string will force it to  be
                # executed and error out if there is a problem.
                str(model.objects.all()[:1].values_list('pk'))
            self.messages.append(self.notice(_("* Database tables are setup properly")))
        except:
            self.errors.append(self.error(_("* Database problem. Try: %s") % "manage.py syncdb"))

    def run_site_check(self):
        e = self.errors.append
        m = self.messages.append
        site_id = settings.SITE_ID
        default_site = "example.com"
        local_site = "localhost:8000"
        admin_url = reverse("admin:sites_site_change", args=(site_id,))
        try:
            site = Site.objects.get(pk=site_id)
        except:
            e(self.error(_("* Problem finding the default site. Perhaps the database isn't setup?")))
            return

        domain = site.domain
        full_url = "%s://%s%s" % (settings.URI_SCHEME, local_site, admin_url)
        snowy_url = "%s://%s" % (settings.URI_SCHEME, domain)

        if domain == default_site:
            e(self.error(_("* Snowy site url is the default of: %s") % domain))
            e(self.error(_("  Try changing it to something like: %s") % local_site))
            e(self.error(_("  Here: %s") % full_url))
        else:
            m(self.notice(_("* Default site has been configured as: %s") % snowy_url))
            m(self.notice(_("  To change the default, go here: %s") % full_url))
