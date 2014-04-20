from pyrate.main import Pyrate
from pyrate.utils import clean_dict


class ListNotFoundError(Exception):
    pass


class MailchimpPyrate(Pyrate):

    # request
    base_url = None  # see __init__
    default_header_content = None
    default_body_content = None  # see __init__
    auth_data = {'type': 'API_KEY'}
    send_json = True

    # response
    response_formats = ['JSON', 'XML', 'PHP']
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'POST', 'target': 'helper/ping'}

    def __init__(self, apikey, default_response_format=None):
        super(MailchimpPyrate, self).__init__()
        self.base_url = 'https://{0}.api.mailchimp.com/2.0/'.format(apikey[-3:])
        self.default_body_content = {
            'apikey': apikey
        }

        if default_response_format:
            self.default_response_format = default_response_format

    def get_auth_data(self):
        return None

    def check_response_success(self, response):
        if 'error' not in response:
            if 'errors' in response:
                if response['errors'] == []:
                    return True
                else:
                    return False
            return True
        else:
            self.parse_errors(response)
            return False

    def parse_errors(self, response):
        if 'error' in response:
            print('Error: {error} (Code: {code})'.format(response))
        elif 'errors' in response:
            for error in response['errors']:
                print('Error: {error} (Code: {code})'.format(error))
                print(error['param'])
        else:
            print('Error: {0}'.format(response))

    # http://apidocs.mailchimp.com/api/2.0/lists/list.php
    def get_all_lists(self, filters=None, start=None, limit=None,
                      sort_field=None, sort_dir=None):

        res = self.post('lists/list', content=clean_dict(locals()))
        if self.check_response_success(res):
            return res['data']
        else:
            return res

    def get_list_by_name(self, list_name):
        lists = self.get_all_lists()
        for l in lists:
            if l['name'] == list_name:
                return l

        raise ListNotFoundError()

    # http://apidocs.mailchimp.com/api/2.0/lists/subscribe.php
    def subscribe_to_list(
            self, list_name, user_email, merge_vars=None, email_type=None,
            double_optin=None, update_existing=None, replace_interests=None,
            send_welcome=None):

        list_id = self.get_list_by_name(list_name)['id']
        kwargs = clean_dict({
            'id': list_id,
            'email': {'email': user_email},
            'merge_vars': merge_vars,
            'email_type': email_type,
            'double_optin': double_optin,
            'update_existing': update_existing,
            'replace_interests': replace_interests,
            'send_welcome': send_welcome,
        })

        return self.post('lists/subscribe', content=kwargs)
        # return self.check_response_success(res)

    # http://apidocs.mailchimp.com/api/2.0/lists/unsubscribe.php
    def unsubscribe_from_list(
            self, list_name, user_email, delete_member=None, send_goodbye=None,
            send_notify=None):

        list_id = self.get_list_by_name(list_name)['id']
        kwargs = clean_dict({
            'id': list_id, 'email': {'email': user_email},
            'delete_member': delete_member, 'send_goodbye': send_goodbye,
            'send_notify': send_notify
        })

        return self.post('lists/unsubscribe', content=kwargs)
        # return self.check_response_success(res)
