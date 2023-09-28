
# Built-ins
from pathlib import Path
from urllib.parse import urlparse, urljoin

# External library packages and modules
from bs4 import BeautifulSoup

# Internal library packages and modules
if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

from extract.extract_model import (
    ArticleSoup,
    remove_formatting,
)


NEXT_BUTTON_JS = "return document.getElementsByClassName('prevnexter')[0];"
URL_QUERY = "documentquery.aspx?Page="


def get_article_urls(page_source, url):
    soup = BeautifulSoup(page_source, 'html.parser')
    articles_links = soup.find_all(attrs={'class': 'newsie-titler'})
    return [urlparse(urljoin(url, h2.find('a')['href'])) for h2 in articles_links if h2.find('a')]


@ArticleSoup.register('title')
def article_title(soup):
    title = soup.find(attrs={'class': 'newsie-titler'})
    return title.get_text(strip=True, separator=' ') if title else None


@ArticleSoup.register('timestamp')
def publish_date(soup):
    date_1 = soup.find('meta', {'property': 'article:published_time'})
    date_2 = soup.find('div', {'class': 'topnewstext'})

    date_1_text = date_1['content'] if date_1 else None
    date_2_text = date_2.get_text(
        strip=True, separator=' ') if date_2 else None

    return date_1_text or date_2_text


@ArticleSoup.register('text')
def article_text(soup):
    content = soup.find('div', {'class': 'newsbody'})
    if content:
        remove_formatting(content)
    return content.get_text(strip=True, separator='\n') if content else None


@ArticleSoup.register('url')
def article_url(soup):
    url = soup.find('meta', {'property': 'og:url'})
    return url['content'] if url else None


@ArticleSoup.register('location')
def article_location(soup):
    location = soup.find('div', {'class': 'topnewstext'})
    return location.get_text(strip=True, separator=' ') if location else None