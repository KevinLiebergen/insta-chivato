#!/usr/bin/python3
import requests
import argparse
import json

class InstagramScraper(object):
    def __init__(self, **kwargs):

        default_attr = dict(username=None, usernames=[], filename=None,
                login_user=None, login_pass=None, logger=None,
                followings_input=False, followings_output='profiles.txt')

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
        login = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        login_text = json.loads(login.text)

        if login_text.get('authenticated') and login.status_code == 200:
            self.authenticated = True
            self.logged_in = True
            self.session.headers.update({'user-agent': CHROME_WIN_UA})
            self.rhx_gis = ""
            print("Connected")
        else:
            print('Login failed for ' + self.login_user)

            
def main():	

    parser = argparse.ArgumentParser(description='Especifica opciones para el script', fromfile_prefix_chars='@')
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
    parser.add_argument('--login-user', '--login_user', '-u', default=None, help='Instagram login user')
    parser.add_argument('--login-pass', '--login_pass', '-p', default=None, help='Instagram login password')

    args = parser.parse_args()
    
    scraper = InstagramScraper(**vars(args))

    if args.login_user and args.login_pass:
        scraper.authenticate_with_login()
    else:
        print("Pon usuario y contraseña")

if __name__ == '__main__':
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    main()
