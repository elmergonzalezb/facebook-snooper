import re
import html
from lxml import html as lxml_html, \
                 etree
from ._text import strip_ml, \
                   sanitize_followers, \
                   get_profile_id


def parse_image(html_text):
    image_link = ''
    matches =  _re.image.findall(html_text)
    if matches:
        image_link = html.unescape(matches[0])
    return image_link


def parse_followers(html_text):
    followers = ''
    matches = _re.followers.findall(html_text)
    if matches:
        followers = sanitize_followers(matches[0])
        followers = followers if followers.isdigit() else ''
    return followers


def parse_intro(html_text):
    items = []
    ul_html = None
    matches = _re.intro.findall(html_text)
    if matches:
        ul_html = matches[0][20:-4]
    if ul_html:
        tree = lxml_html.fromstring(ul_html)
        for intro in tree.xpath('//li/*[1]/div/div/div'):
            fragment = etree.tostring(intro).decode("utf-8")
            info = html.unescape(strip_ml(fragment))
            items.append(info)           
    return items


def parse_search_result(html_text):
    results = []
    # Rip JavaScript dictionary data
    profileURIs = re.findall(r'profileURI:".+?"', html_text)
    texts = re.findall(r'text:".+?"', html_text)
    if profileURIs:
        for i, profileURI in enumerate(profileURIs):
            profile_uri = html.unescape(profileURI[12:-1])
            if not '/groups/' in profile_uri and \
               not '/events/' in profile_uri:
                profile_id = get_profile_id(profile_uri)
                profile_name = texts[i][6:-1]
                results.append((profile_id, profile_name, profile_uri))
    return results


class _re:
    followers = re.compile(r'frankbruninyt/followers.*people', re.MULTILINE)
    image = re.compile(r'photoContainer.+?img.+?src="(.+?)"')
    intro = re.compile(r'intro_container_id.+?</ul')