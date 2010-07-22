from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def user_index(request, username):
    if request.user.is_authenticated() and str(request.user) == str(username):
        return HttpResponseRedirect(reverse("note_index", args=([username])))
    else:
        return HttpResponseRedirect(reverse("snowy_index"))
