from six import iteritems
from six.moves import urllib

from requests_oauthlib import OAuth1


def build_oauth1(client_key, client_secret, resource_owner_key,
                 resource_owner_secret):
    return OAuth1(client_key=client_key, client_secret=client_secret,
                  resource_owner_key=resource_owner_key,
                  resource_owner_secret=resource_owner_secret)


def clean_dict(dirty_dict):
    """Cleans a dictionary from keys with empty string values"""
    return dict((k, v) for k, v in iteritems(dirty_dict) if v)


def append_qs(url, items):
    """Append a key/value to the query string of a url"""

    if not items:
        return url

    u = urllib.parse.urlsplit(url)
    qsl = urllib.parse.parse_qsl(u.query)

    if isinstance(items, dict):
        qsl = qsl + items.items()
    elif isinstance(items, list):
        qsl = qsl + items
    elif isinstance(items, tuple):
        qsl.append(items)

    return u._replace(query=urllib.urlencode(qsl)).geturl()


# Deprecated methods
def build_basic_auth(*args, **kwargs):
    raise DeprecationWarning('This method is deprecated since python-requests '
                             'is able to do the same.')
