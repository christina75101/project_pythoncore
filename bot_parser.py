import feedparser
from enum import Enum
from telegraph import Telegraph
from configparser import ConfigParser
from pathlib import Path


config_file = ConfigParser()
path = str(Path(__file__).parent / 'config.ini')
config_file.read(path)


class Site(Enum):
    BASH_ORG = 'bash.im'
    KILL_ME_PLS = 'killpls.me'
    ZADOLBALI = 'zadolba.li'


def parse_rss(site, entry_num=0):
    """
    Method parses given site

    Parameters
    ----------
    site: Site
        Enumerated constant that represent web site we will work with
    entry_num: int
        Number of entry we are interesting in, 0 by default

    Returns
    -------
    dict
        The dictionary with title, title_id, source and text (reformatted for the bash.im)

    """
    url = 'https://{}/rss'.format(site.value)
    feed = feedparser.parse(url)
    title_id = feed.entries[entry_num].id
    title = feed.entries[entry_num].title
    text = feed.entries[entry_num].description
    if site == Site.BASH_ORG or site == Site.KILL_ME_PLS:
        text = text.replace("<br>", "\n")
        text = text.replace("&quot;", "\"")

    return dict(title_id=title_id, title=title, source=site, text=text)


def create_telegraph_article(title, content, author):
    """
    Method creates article in telegra.ph thru the api, using title, author and text of article

    Parameters
    ----------
    title: str
    content: str
        text formatted in html
    author: str

    Returns
    -------
    str
        url link to the article

    """
    access_token = config_file['TELEGRAPH']['api_token']
    telegraph = Telegraph(access_token=access_token)
    response = telegraph.create_page(author_name=author, title=title, html_content=content)
    return 'https://telegra.ph/{}'.format(response['path'])


def get_preformatted_text(site, entry_num=0):
    """
        Simple api to get preprocessed text, already formatted to send through the Telegram bot

    Parameters
    ----------
    site: Site
        Enumerated constant that represent web site we will work with
    entry_num: int
        Number of entry we are interesting in, 0 by default

    Returns
    -------
    str
        Formatted string ready to send thru the bot

    Raises
    ------
    NotImplementedError
        in case when unexpected site is given

    """
    parsed_feed = parse_rss(site=site, entry_num=entry_num)

    if site == Site.ZADOLBALI:
        tel = create_telegraph_article(title=parsed_feed['title'], content=parsed_feed['text'], author=site.name)
        text = '<b>{}</b> \nscr - <i>{}</i> \n<a href="{}">read</a>'.format(parsed_feed['title'], site.value, tel)
        return text
    elif site == Site.BASH_ORG or site == Site.KILL_ME_PLS:
        text = '<b>{}</b> \nscr - <i>{}</i> \n{}'.format(parsed_feed['title'], site.value, parsed_feed['text'])
        return text
    else:
        raise NotImplementedError


if __name__ == '__main__':

    txt = get_preformatted_text(site=Site.BASH_ORG)

    print(txt)
