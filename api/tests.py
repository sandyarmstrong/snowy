import urllib
import base64

# Use simplejson or Python 2.6 json, prefer simplejson.
try:
    import simplejson as json
except ImportError:
    import json

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.utils.functional import curry

from piston import oauth
from piston.models import Consumer, Token
from piston.forms import OAuthAuthenticationForm

from snowy import settings
from snowy.notes.models import Note

class OAuthRequester:
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

    def __init__ (self, test_case, username, password, consumer):
        self.SERVER_NAME = 'testserver'
        self.consumer = consumer
        self.test_case = test_case
        
        # Much of this method comes straight from Piston's unit tests
        # TODO: Fix copyright, then!
        oaconsumer = oauth.OAuthConsumer(self.consumer.key,
                                         self.consumer.secret)

        # Get a request key...
        url = 'http://' + self.SERVER_NAME + '/oauth/request_token/'
        request = oauth.OAuthRequest.from_consumer_and_token(oaconsumer,
                                                             http_url=url)
        request.sign_request(self.signature_method, oaconsumer, None)

        response = test_case.client.get('/oauth/request_token/',
                                        request.parameters)
        oatoken = oauth.OAuthToken.from_string(response.content)

        token = Token.objects.get(key=oatoken.key, token_type=Token.REQUEST)
        test_case.assertEqual(token.secret, oatoken.secret)

        # Simulate user authentication...
        test_case.failUnless(test_case.client.login(username=username,
                                                    password=password))
        url = 'http://' + self.SERVER_NAME + '/oauth/authenticate/'
        c_url = 'http://printer.example.com/request_token_ready'
        request = oauth.OAuthRequest.from_token_and_callback(token=oatoken,
                                                             callback=c_url,
                                                             http_url=url)
        request.sign_request(self.signature_method, oaconsumer, oatoken)
        
        # Faking form submission seems to not work, so approve token manually
        token.is_approved = True
        token.user = User.objects.get(username=username)
        token.save()

        # Obtain access token...
        url = 'http://' + self.SERVER_NAME + '/oauth/access_token/'
        request = oauth.OAuthRequest.from_consumer_and_token(oaconsumer,
                                                             token=oatoken,
                                                             http_url=url)
        request.sign_request(self.signature_method, oaconsumer, oatoken)
        response = test_case.client.get('/oauth/access_token/',
                                        request.parameters)

        oa_atoken = oauth.OAuthToken.from_string(response.content)
        atoken = Token.objects.get(key=oa_atoken.key, token_type=Token.ACCESS)
        test_case.assertEqual(atoken.secret, oa_atoken.secret)

        self.oa_atoken = oa_atoken

    def build_request(self, abs_uri, method):
        url = 'http://' + self.SERVER_NAME + abs_uri
        oaconsumer = oauth.OAuthConsumer(self.consumer.key,
                                         self.consumer.secret)
        request = oauth.OAuthRequest.from_consumer_and_token(oaconsumer,
                                                             token=self.oa_atoken,
                                                             http_url=url,
                                                             http_method=method)
        request.sign_request(self.signature_method, oaconsumer, self.oa_atoken)
        return request

    def build_auth_header(self, request):
        return request.to_header(realm='Snowy')['Authorization']

    def get(self, abs_uri):
        request = self.build_request(abs_uri, 'GET')
        auth = self.build_auth_header(request)
        return self.test_case.client.get(abs_uri,
                                         HTTP_AUTHORIZATION=auth)

    def put(self, abs_uri, json):
        request = self.build_request(abs_uri, 'PUT')
        auth = self.build_auth_header(request)
        return self.test_case.client.put(abs_uri, data=json,
                                         content_type='application/json',
                                         HTTP_AUTHORIZATION=auth)

    def post(self, abs_uri, json):
        request = self.build_request(abs_uri, 'POST')
        auth = self.build_auth_header(request)
        return self.test_case.client.post(abs_uri, data=json,
                                          content_type='application/json',
                                          HTTP_AUTHORIZATION=auth)

    def delete(self, abs_uri):
        request = self.build_request(abs_uri, 'DELETE')
        auth = self.build_auth_header(request)
        return self.test_case.client.delete(abs_uri,
                                            HTTP_AUTHORIZATION=auth)


class ApiTestCase(TestCase):
    fixtures = ['basic.json']

    def setUp(self):
        # Although client.put now exists in Django 1.1, it is unusable for us:
        # http://code.djangoproject.com/ticket/11371
        # So, we override it with our own working version:
        self.client.put = curry(self.client.post, REQUEST_METHOD='PUT')
        # TODO: Use standard consumer?
        self.consumer = Consumer(name='Test Consumer', description='Test',
                                 status='accepted')
        self.consumer.key="123"
        self.consumer.secret="123"
        self.consumer.save()
        self.admin_requester = OAuthRequester(self, 'admin', 'admin',
                                              self.consumer)
        self.test1_requester = OAuthRequester(self, 'test1', 'test1',
                                              self.consumer)

    def tearDown(self):
        self.consumer.delete()

    def testUser(self):
        # Test a user with missing fields
        response = self.client.get('/api/1.0/admin/')
        self.assertEqual(response.status_code, 200)
        # TODO: Genericize URL stuff
        self.assertEqual(json.loads(response.content),
                         {
                            'user-name': 'admin',
                            'last-name': '',
                            'notes-ref': {
                                'href': 'http://example.com/admin/notes/',
                                'api-ref':
                                    'http://example.com/api/1.0/admin/notes/'
                            },
                            'current-sync-guid':
                                '5ec1f08a-19f1-416a-b086-ff22f6f7c9e8',
                            'first-name': '',
                            'latest-sync-revision': -1
                         })

        # Test a user with all fields, with and without auth
        for client in self.client, self.test1_requester:
            response = client.get('/api/1.0/test1/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.content),
                             {'user-name': 'test1',
                              'last-name': 'Doe',
                              'notes-ref': {
                                'href': 'http://example.com/test1/notes/',
                                'api-ref':
                                    'http://example.com/api/1.0/test1/notes/'
                              },
                              'current-sync-guid':
                                '1886ae92-6c46-43e8-86c0-bb74df89f66c',
                              'first-name': 'John',
                              'latest-sync-revision': -1
                             })


    def testUserBadMethods(self):
        # PUT/POST/DELETE are not allowed
        # POST and PUT need some dummy data, otherwise piston replies "Bad Request"
        response = self.admin_requester.put('/api/1.0/admin/', '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.post('/api/1.0/admin/', '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.delete('/api/1.0/admin/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')


    def testRootNoAuth(self):
        # Test w/out auth
        response = self.client.get('/api/1.0/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content),
                         {
                            'api-version': '1.0',
                            'oauth_access_token_url': 'http://example.com/oauth/access_token/',
                            'oauth_authorize_url': 'http://example.com/oauth/authenticate/',
                            'oauth_request_token_url': 'http://example.com/oauth/request_token/'
                         })

    def testRootWithAuth(self):
        # Test w/ auth (admin user)
        response = self.admin_requester.get('/api/1.0/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content),
                         {
                            'api-version': '1.0',
                            'user-ref': {
                                'href': 'http://example.com/admin/',
                                'api-ref': 'http://example.com/api/1.0/admin/'
                            },
                            'oauth_access_token_url': 'http://example.com/oauth/access_token/',
                            'oauth_authorize_url': 'http://example.com/oauth/authenticate/',
                            'oauth_request_token_url': 'http://example.com/oauth/request_token/'
                         })

        # Test w/ auth (test1 user)
        response = self.test1_requester.get('/api/1.0/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content),
                         {
                            'api-version': '1.0',
                            'user-ref': {
                                'href': 'http://example.com/test1/',
                                'api-ref': 'http://example.com/api/1.0/test1/'
                            },
                            'oauth_access_token_url': 'http://example.com/oauth/access_token/',
                            'oauth_authorize_url': 'http://example.com/oauth/authenticate/',
                            'oauth_request_token_url': 'http://example.com/oauth/request_token/'
                         })


    def testRootBadMethods(self):
        # PUT/POST/DELETE are not allowed
        # POST and PUT need some dummy data, otherwise piston replies "Bad Request"
        response = self.admin_requester.put('/api/1.0/', '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.post('/api/1.0/', '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.delete('/api/1.0/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        
    def testNotes(self):
        noteJson = '{"guid": "002e91a2-2e34-4e2d-bf88-21def49a7705",' + \
                   '"title" :"New Note 6",' + \
                   '"note-content" :"New Note 6\\nDescribe youre note <b>here</b>.",' + \
                   '"note-content-version" : 0.2,' + \
                   '"last-change-date" : "2009-04-19T21:29:23.2197340-07:00",' + \
                   '"last-metadata-change-date" : "2009-04-19T21:29:23.2197340-07:00",' + \
                   '"create-date" : "2008-03-06T13:44:46.4342680-08:00",' + \
                   '"last-sync-revision" : 0,' + \
                   '"open-on-startup" : false,' + \
                   '"tags" : ["tag1","tag2"]' + \
                   '}'
        notesJson = '{"latest-sync-revision" : 0,' + \
                    '"note-changes" : [' + noteJson + ']}'

        full_notes = {
                        "notes": [
                            {
                                "guid": "002e91a2-2e34-4e2d-bf88-21def49a7705", 
                                "ref": {
                                    "href": "http://example.com/admin/notes/1/", 
                                    "api-ref": "http://example.com/api/1.0/admin/notes/1/"
                                }, 
                                "title": "New Note 6"
                            }
                        ], 
                        "latest-sync-revision": 0
                    }
        public_notes = {
                        "notes": [], 
                        "latest-sync-revision": 0
                    }

        response = self.admin_requester.put ('/api/1.0/admin/notes/', notesJson)
        self.assertEqual(json.loads(response.content), full_notes)

        response = self.client.get('/api/1.0/admin/notes/')
        self.assertEqual(response.status_code, 401)

        response = self.admin_requester.get('/api/1.0/admin/notes/')
        self.assertEqual(json.loads(response.content), full_notes)

        response = self.test1_requester.get('/api/1.0/admin/notes/')
        self.assertEqual(json.loads(response.content), public_notes)

        # Make a note public
        # TODO: Test collections with a mix of public and private notes
        admin = User.objects.get(username='admin')
        note = Note.objects.get(author=admin,
                                guid="002e91a2-2e34-4e2d-bf88-21def49a7705")
        note.permissions=1
        note.save()

        response = self.test1_requester.get('/api/1.0/admin/notes/')
        self.assertEqual(json.loads(response.content), full_notes)


    def testNotesBadMethods(self):
        # POST/DELETE are not allowed
        # POST and PUT need some dummy data, otherwise piston replies "Bad Request"
        response = self.admin_requester.post('/api/1.0/admin/notes/',  '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET, PUT')
        response = self.admin_requester.delete('/api/1.0/admin/notes/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET, PUT')

    def testNote(self):
        # TODO
        pass

    def testNoteBadMethods(self):
        # PUT/POST/DELETE are not allowed
        # POST and PUT need some dummy data, otherwise piston replies "Bad Request"
        response = self.admin_requester.put('/api/1.0/admin/notes/1/',  '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.post('/api/1.0/admin/notes/1/',  '{ "test" : "test" }')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
        response = self.admin_requester.delete('/api/1.0/admin/notes/1/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')
