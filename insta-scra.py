#!/usr/bin/python3
import requests

class InstagramScraper(object):
    def __init__(self, **kwargs):

        default_attr = dict(username='', usernames=[], filename=None,
                login_user=None, login_pass=None,
                followings_input=False, followings_output='profiles.txt',
                destination='./', logger=None, retain_username=False, interactive=False,
                quiet=False, maximum=0, media_metadata=False, profile_metadata=False, latest=False,
                latest_stamps=False, cookiejar=None, filter_location=None, filter_locations=None,
                media_types=['image', 'video', 'story-image', 'story-video'],
                tag=False, location=False, search_location=False, comments=False,
                verbose=0, include_location=False, filter=None, proxies={}, no_check_certificate=False,
                                                                        template='{urlname}', log_destination='')
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
            self.logger.error('Login failed for ' + self.login_user)

            if 'checkpoint_url' in login_text:
                checkpoint_url = login_text.get('checkpoint_url')
                self.logger.error('Please verify your account at ' + BASE_URL[0:-1] + checkpoint_url)

                if self.interactive is True:
                    self.login_challenge(checkpoint_url)
            elif 'errors' in login_text:
                for count, error in enumerate(login_text['errors'].get('error')):
                    count += 1
                    self.logger.debug('Session error %(count)s: "%(error)s"' % locals())
            else:
                self.logger.error(json.dumps(login_text))

def main():	
    scraper = InstagramScraper()
    scraper.authenticate_with_login()




if __name__ == '__main__':
    BASE_URL = 'https://www.instagram.com/'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    main()
