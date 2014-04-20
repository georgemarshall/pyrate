from pyrate.main import Pyrate
from pyrate.utils import clean_dict


class OrganisationNotFoundError(Exception):
    pass


class GithubPyrate(Pyrate):

    # request
    base_url = 'https://api.github.com/'
    default_header_content = None  # see __init__
    default_body_content = None
    auth_data = {'type': 'BASIC', 'username': None, 'password': None}
    send_json = True

    # response
    response_formats = []
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': '#'}

    def __init__(self, auth_user, auth_pass, default_response_format=None):
        super(GithubPyrate, self).__init__()
        self.auth_data['username'] = auth_user
        self.auth_data['password'] = auth_pass
        self.default_header_content = {
            'Authorization': self.get_auth_data()
        }

        if default_response_format:
            self.default_response_format = default_response_format

    def get_my_orgs(self):
        return self.get('user/orgs')

    def create_repo(self, name, description=None, org_name=None, private=None):
        kwargs = clean_dict({'name': name, 'description': description,
                             'private': private})

        target = 'orgs/{0}/repos'.format(org_name) if org_name else 'user/repos'

        return self.post(target, content=kwargs)

    def delete_repo(self, name, org_name=None):
        user = str(org_name) if org_name else self.auth_data['username']

        return self.delete('repos/{0}/{1}'.format(user, name))
