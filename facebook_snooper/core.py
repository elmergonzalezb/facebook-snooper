from abc import ABC, \
                abstractmethod
import os.path
from mechanicalsoup import StatefulBrowser, \
                           LinkNotFoundError
from . import _parser


class SnooperException(Exception):
    pass


class Session:
    def __init__(self):
        self._connected = False
        self._current_html = None

    @property
    def current_html(self):
        """Current page HTML for testing purposes."""
        return self._current_html

    @property
    def connected(self):
        return self._connected

    def _ensure_connected(self):
        if not self._connected:
            raise SnooperException("No active connection or valid login")

    @abstractmethod
    def _get_current_title(self):
        pass

    @abstractmethod
    def _get_profile_html(self, profile_id):
        pass

    @abstractmethod
    def _get_search_html(self, query):
        pass

    @staticmethod
    def default():
        return _FacebookSession()

    @abstractmethod
    def log_in(self, username, password):
        """Log in to facebook with username and password."""
        pass

    def profile_info(self, profile_id):
        """Retrieve informations for a given profile."""
        self._ensure_connected()
        try:
            profile_html = self._get_profile_html(profile_id)
            name  = self._get_current_title()
            intro =  _parser.parse_intro(profile_html)
            followers = _parser.parse_followers(profile_html)
            return name, followers, intro
        except:
            return None

    def search_profiles(self, query):
        """Search profiles that match given query, returning a tuple with ID and URI."""
        self._ensure_connected()
        try:
            return _parser.parse_search_result(self._get_search_html(query))
        except:
            return None


class _FacebookSession(Session):
    def log_in(self, username, password):
        self._base_url = 'https://www.facebook.com'
        try:
            self._browser = StatefulBrowser()
            self._browser.addHeaders = [
                    ('User-Agent', 'Firefox'), \
                    ('Accept-Language', 'en-US,en;q=0.5')
                    ]
            self._browser.open(self._base_url)
            self._current_html = str(self._browser.get_current_page())
            self._browser.select_form('form[id="login_form"]')
            self._browser['email'] = username
            self._browser['pass'] =  password        
            self._browser.submit_selected()
            self._browser.select_form('form[action="/search/top/"]')
            self._connected = True
        except:
             self._connected = False
        return self._connected

    def _get_current_title(self):
        return self._browser.get_current_page().find('title').text

    def _get_profile_html(self, profile_id):
        url = f'{self._base_url}/{profile_id}'
        self._browser.open(url)
        self._current_html = str(self._browser.get_current_page())
        return self._current_html

    def _get_search_html(self, query):
        self._browser.select_form('form[action="/search/top/"]')
        self._browser['q'] = query
        self._browser.submit_selected()
        self._current_html = str(self._browser.get_current_page())
        return self._current_html