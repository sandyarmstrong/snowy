class ReCaptchaMiddleware(object):
    """
    A tiny middleware to automatically add IP address to ReCaptcha
    POST requests
    """
    def process_request(self, request):
        if request.method == 'POST' and \
           'recaptcha_challenge_field' in request.POST and \
           'recaptcha_ip_field' not in request.POST:
            data = request.POST.copy()
            data['recaptcha_ip_field'] = request.META['REMOTE_ADDR']
            request.POST = data
