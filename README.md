# Facebook Snooper

Scrapes Facebook profile pages using a normal log in (without an API key). Inspired by [facebook-scraper](https://github.com/kevinzg/facebook-scraper).

## Install
```sh
$ wget https://raw.githubusercontent.com/gsscoder/facebook-snooper/master/facebook_snooper.py
```

## Usage
```python
>>> from facebook_snooper import log_in
>>> from facebook_snooper import get_intro
>>> log_in('user@email.com', 'user_password')
True
>>> get_intro('fb.profile.id')
['Works at ...', 'Former consultant at ...', 'Studies at Columbia University', 'Went to UNC Chapel Hill', 'Lives in White Plains, New York', 'Joined August 2015', 'Followed by 1,068 people']
```

## Test
Create test folder and data:
```sh
$ cd facebook_snooper
$ mkdir test-data
```
```python
>>> from facebook_snooper import _test_save_html, _get_intro_html
>>> from facebook_snooper import log_in
>>> log_in('user@email.com', 'user_password')
True
>>> _test_save_html('profile', _get_intro_html('fb.profile.id'))
```
Execute test script:
```sh
$ python test.py
```

### Disclaimer
- Respect people's privacy! This code was written for demonstration purposes.

### Notes
- There is no guarantee that will work if scraped pages change too much.