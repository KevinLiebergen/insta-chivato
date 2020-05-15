#!/usr/bin/python3
import requests
import argparse
import json


class InstagramScraper(object):
    def __init__(self, **kwargs):

        default_attr = dict(username=None, usernames=[], filename=None, logged_in=None,
                            login_user=None, login_pass=None, logger=None, login_text=None)

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        self.session = requests.Session()


    def authenticate_with_login(self):
        """Logs in to instagram."""
        self.session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
        req = self.session.get(BASE_URL)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login_data = {'username': self.login_user, 'password': self.login_pass}
        login = self.session.post(
            LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update(
            {'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
#        print('***** cookie de session id: {}'.format(self.cookies['sessionid']))
        self.login_text = json.loads(login.text)

        if self.login_text.get('authenticated') and login.status_code == 200:
            self.authenticated = True
            self.logged_in = True
            self.session.headers.update({'user-agent': MY_UA})
            self.rhx_gis = ""
        else:
            print('Login failed for ' + self.login_user)


    def count_people(self, query, edge):
        maxim = 50

        # Elige user_id del username
        if self.username == []:
            user_id = self.login_text['userId']
        else:
            url_username = '{}{}/?__a=1'.format(BASE_URL, self.username[0])
            response = requests.get(url_username)
            user_id = response.json()['graphql']['user']['id']

        url = '{0}graphql/query/?query_hash={1}&variables=%7B%22id%22%3A%22{2}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A{3}%7D'.format(BASE_URL, query, user_id, maxim)
        self.url_orig = url

        sessionid = self.cookies['sessionid']

        header = {'Cookie': 'sessionid={}'.format(sessionid) } ### Cambiar esto
        people = []
        
        return self.recursive_count(url, header, edge, people)


    def recursive_count(self, url, header, edge, people):
        r = requests.get(url, headers=header)

        for user in r.json()['data']['user'][edge]['edges']:
            people.append(user['node']['username'])

        if r.json()['data']['user'][edge]['page_info']['has_next_page'] == True:
            # Capturas la direccion de la proxima consulta
            after = r.json()['data']['user'][edge]['page_info']['end_cursor']
            # [:-3] quitas el %7D que es '}'
            url = self.url_orig[:-3] + '%2c%22after%22%3A%22' + after + '%22%7D'

            self.recursive_count(url, header, edge, people)
        return people


    def get_following(self):
        query_hash_following='d04b0a864b4b54837c0d870b0e77e076'
        edge = 'edge_follow'
        return self.count_people(query_hash_following, edge)


    def get_followers(self):
        query_hash_followers='c76146de99bb02f6415203be841dd25a'
        edge = 'edge_followed_by'
        return self.count_people(query_hash_followers, edge)


    def logout(self):
        """Logs out of instagram."""
        if self.logged_in:
            try:
                logout_data = {'csrfmiddlewaretoken': self.cookies['csrftoken']}
                self.session.post(LOGOUT_URL, data=logout_data)
                self.authenticated = False
                self.logged_in = False
                print("Sesion cerrada")
            except requests.exceptions.RequestException:
                self.logger.warning('Failed to log out ' + self.login_user)


    def compare_people(self, following, followers):
        main_list = list(set(following) - set(followers))
        print(main_list)
        #return dfollowback


def main():

    parser = argparse.ArgumentParser(
        description='Especifica opciones para el script', fromfile_prefix_chars='@')
    '''
        You can hide your credentials from the history, by reading your
        username from a local file:
        $ instagram-scraper @insta_args.txt user_to_scrape
        with insta_args.txt looking like this:
        -u=my_username
        -p=my_password
        You can add all arguments you want to that file, just remember to have
        one argument per line.
    '''
    parser.add_argument('username', help='Instagram user(s) to scrape', nargs='*')
    parser.add_argument('--login-user', '--login_user', '-u',
                        default=None, help='Instagram login user')
    parser.add_argument('--login-pass', '--login_pass', '-p',
                        default=None, help='Instagram login password')

    args = parser.parse_args()

    scraper = InstagramScraper(**vars(args))

    if args.login_user and args.login_pass:
        scraper.authenticate_with_login()
    else:
        raise ValueError("Pon usuario y contraseña")

    try:
        following = scraper.get_following()
        #print(following)
        followers = scraper.get_followers()
        #print(followers)
        dfollowback = scraper.compare_people(following, followers)
        #print(dfollowback)
    finally:
        scraper.logout()


if __name__ == '__main__':
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    MY_UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    LOGOUT_URL = BASE_URL + 'accounts/logout/'
    main()
