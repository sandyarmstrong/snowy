#
# Copyright (c) 2010 Sander Dijkhuis <sander.dijkhuis@gmail.com>
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

from django.core.management.base import NoArgsCommand, CommandError

import smtpd

class MailDebuggingServer(smtpd.DebuggingServer):
    skip_headers = ('Content-Type', 'MIME-Version', 'Content-Transfer-Encoding',
        'Message-ID')

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('\n----------- BEGIN MESSAGE -----------')

        (headers, body) = data.split('\n\n', 1)
        quoted_printable = False

        for header in headers.split('\n'):
            if header == 'Content-Transfer-Encoding: quoted-printable':
                quoted_printable = True

            if not header.split(':')[0] in self.skip_headers:
                print(header)

        print('')

        if quoted_printable:
            import quopri

            print(quopri.decodestring(body))
        else:
            print(body)

        print('------------ END MESSAGE ------------')

class Command(NoArgsCommand):
    help = "Run a mail debugging server, matching the project settings"

    def handle_noargs(self, **options):
        from django.conf import settings

        import asyncore
        import socket

        host_port = (settings.EMAIL_HOST, settings.EMAIL_PORT)

        try:
            server = MailDebuggingServer(host_port, None)
        except socket.error:
            raise CommandError('Could not set up the mail server at %s:%d.\n'
                % host_port
                + 'Make sure that you can actually host a server using the\n'
                + 'current values for settings.EMAIL_HOST and settings.EMAIL_PORT.')

        print('Mail debugging server is running at %s:%d' % host_port)
        print('Emails from this Django site will appear here instead of being sent.')
        print('Quit the server with CONTROL-C.')

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            # Print a blank line after the ^C. This looks nicer.
            print('')

            pass
