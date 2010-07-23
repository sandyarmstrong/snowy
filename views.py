from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def user_index(request, username):
    return HttpResponseRedirect(reverse("note_index", args=([username])))
