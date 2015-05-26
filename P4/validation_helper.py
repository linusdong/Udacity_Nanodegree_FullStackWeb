import endpoints
from google.appengine.ext import ndb
def validate_conf_key(websafeConferenceKey):
    """validate single conference key.
       Input: websafeConferenceKey
       Output: conference key"""
    wsck = websafeConferenceKey
    c_key = ndb.Key(urlsafe=wsck)
    if not c_key:
        raise endpoints.NotFoundException(
            'No conference found with key: %s' % wsck)
    if c_key.kind() != 'Conference':
        raise endpoints.BadRequestException(
            'Please provide correct conference key.\n'
            'Error key: %s' % wsck)
    return c_key
