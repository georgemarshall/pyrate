from urllib import urlencode
from urlparse import parse_qsl, urlsplit

from requests_oauthlib import OAuth1


def build_oauth1(client_key, client_secret, resource_owner_key,
                 resource_owner_secret):
    return OAuth1(client_key=client_key, client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret)


def clean_dict(dirty_dict):
    """Cleans a dictionary from keys with empty string values"""
    return dict((k, v) for k, v in dirty_dict.iteritems() if v)


def append_qs(target, key, value=''):
    """Append a key/value to the query string of a url"""
    url = urlsplit(target)
    qsl = parse_qsl(url.query)
    qsl.append((key, value))

    return url._replace(query=urlencode(qsl)).geturl()


# Deprecated methods
def build_basic_auth(*args, **kwargs):
    raise DeprecationWarning('This method is deprecated since python-requests '
                             'is able to do the same.')
