from django import http
from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def user_index(request, username):
    return HttpResponseRedirect(reverse("note_index", args=([username])))

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))
