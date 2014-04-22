from pyrate.main import Pyrate
from pyrate.utils import append_qs, clean_dict


class YelpPyrate(Pyrate):

    # request
    base_url = 'https://api.yelp.com/v2/'
    default_header_content = None
    default_body_content = None
    auth_data = {
        'type': 'OAUTH1',
        'client_key': None, 'client_secret': None,
        'token_key': None, 'token_secret': None
    }
    send_json = False

    # response
    response_formats = ['json']
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': None, 'target': None}

    def __init__(self, oauth_consumer_key, oauth_consumer_secret, oauth_token,
                 oauth_token_secret, default_response_format=None):
        super(YelpPyrate, self).__init__()
        self.auth_data['client_key'] = oauth_consumer_key
        self.auth_data['client_secret'] = oauth_consumer_secret
        self.auth_data['token_key'] = oauth_token
        self.auth_data['token_secret'] = oauth_token_secret

        if default_response_format:
            self.default_response_format = default_response_format

    # Convenience
    def get_business(self, name, country_code=None, language=None,
                     language_filter=None):

        qs = clean_dict({
            'cc': country_code,
            'lang': language,
            'lang_filter': language_filter
        })

        target = append_qs('business/{0}'.format(name), qs)

        return self.get(target)

    def search(self, term=None, limit=None, offset=None, sort=None,
               category_filter=None, radius_filter=None, deals_filter=None,
               country_code=None, language=None, **kwargs):

        qs = clean_dict({
            'term': term,
            'limit': limit,
            'offset': offset,
            'sort': sort,
            'category_filter': category_filter,
            'radius_filter': radius_filter,
            'deals_filter': deals_filter,
            'cc': country_code,
            'lang': language
        })

        target = append_qs('search', qs)

        return self.get(target)
