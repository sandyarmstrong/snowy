"""
recaptcha-django

ReCAPTCHA (Completely Automated Public Turing test to tell Computers and
Humans Apart - while helping digitize books, newspapers, and old time radio
shows) module for django
"""

from django.forms import Widget, Field, ValidationError
from django.conf import settings
from django.utils.translation import get_language
from django.utils.html import conditional_escape
from recaptcha.client import captcha
from django.utils.safestring import mark_safe

class ReCaptchaWidget(Widget):
    """
    A Widget that renders a ReCAPTCHA form
    """
    options = ['theme', 'lang', 'custom_theme_widget', 'tabindex']

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        error = final_attrs.get('error', None)
        html = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, error=error)
        options = u',\n'.join([u'%s: "%s"' % (k, conditional_escape(v)) \
                   for k, v in final_attrs.items() if k in self.options])
        return mark_safe("""<script type="text/javascript">
        var RecaptchaOptions = {
            %s
        };
        </script>
        %s
        """ % (options, html))


    def value_from_datadict(self, data, files, name):
        """
        Generates Widget value from data dictionary.
        """
        try:
            return {'challenge': data['recaptcha_challenge_field'],
                    'response': data['recaptcha_response_field'],
                    'ip': data['recaptcha_ip_field']}
        except KeyError:
            return None
        
class ReCaptchaField(Field):
    """
    Field definition for a ReCAPTCHA
    """
    widget = ReCaptchaWidget

    def clean(self, value):
        resp = captcha.submit(value.get('challenge', None),
                              value.get('response', None),
                              settings.RECAPTCHA_PRIVATE_KEY,
                              value.get('ip', None))
        if not resp.is_valid:
            self.widget.attrs['error'] = resp.error_code 
            raise ValidationError(resp.error_code)
