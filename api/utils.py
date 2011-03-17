import base64

from django.conf import settings

def check_credentials(request_metadata):
    if request_metadata.has_key('HTTP_AUTHORIZATION'):
        authorization = request_metadata['HTTP_AUTHORIZATION']
        authorization = authorization.replace('Basic ', '')
        credentials = base64.decodestring(authorization).split(':')

        if (credentials[0] != settings.API_USERNAME or
            credentials[1] != settings.API_PASSWORD):
            raise ValueError('Invalid credentials')
    else:
        raise ValueError('Missing credentials')
