#!/usr/bin/python3
import requests
import argparse
import json


class InstagramScraper(object):
    def __init__(self, **kwargs):

        default_attr = dict(username=None, usernames=[], filename=None,
                            login_user=None, login_pass=None, logger=None, login_text=None,
                            followings_input=False, followings_output='profiles.txt')

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        self.session = requests.Session()

    def authenticate_with_login(self):
        """Logs in to instagram."""
        self.session.headers.update({'Referer': BASE_URL, 'user-agent': MY_UA})
        req = self.session.get(BASE_URL)
        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login_data = {'username': self.login_user, 'password': self.login_pass}
        login = self.session.post(
            LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update(
            {'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        self.login_text = json.loads(login.text)

        if self.login_text.get('authenticated') and login.status_code == 200:
            self.authenticated = True
            self.logged_in = True
            self.session.headers.update({'user-agent': MY_UA})
            self.rhx_gis = ""
            print("Connected")
        else:
            print('Login failed for ' + self.login_user)

    def get_following(self):
        query_hash='d04b0a864b4b54837c0d870b0e77e076'
        user_id = self.login_text['userId']
        maxim = 50

        '''
curl 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22504242447%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A2%7D' -H 'Cookie: sessionid=504242447%3AujedbYp2BYfxEr%3A11' 
        '''
        

        url = '{}graphql/query/?query_hash={}&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A{}%7D'.format(BASE_URL, query_hash, user_id, maxim)

        url = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22504242447%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A2%7D'
        header = {'Cookie': 'sessionid=504242447%3AujedbYp2BYfxEr%3A11' }
        r = requests.get(url, headers=header)
        print(r.content())


#        return following


    def get_followers(self):

        return followers


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

    scraper.get_following()

if __name__ == '__main__':
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    MY_UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    main()
