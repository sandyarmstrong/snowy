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

from snowy.core.urlresolvers import reverse_full

from django import template

register = template.Library()

@register.tag
def full_url(parser, tokens):
    """ Usage:
        {% full_url view <same args as for url> %}
    """
    tokens = tokens.split_contents()
    if len(tokens) < 3:
        raise template.TemplateSyntaxError, \
            "%r tag requires at least two arguments" % tokens[0]

    args = []
    for arg in tokens[2:]:
        args.append(parser.compile_filter(arg))

    return FullUrlNode(tokens[1], args)

class FullUrlNode(template.Node):
    def __init__(self, view, args):
        self.view = view
        self.args = args

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        return reverse_full(self.view, args=args)
