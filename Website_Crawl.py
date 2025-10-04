import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

START_URL = "https://prathameshdeshmukh.site"
visited = set()
site_map = []
external_links = set()
all_internal_links = set()
linked_internal_links = set()
extra_internal_urls = set()

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag['href'])
            parsed_link = urlparse(link)
            start_netloc = urlparse(START_URL).netloc
            if parsed_link.netloc == start_netloc:
                clean_link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path
                all_internal_links.add(clean_link)
                linked_internal_links.add(clean_link)
                if clean_link not in visited:
                    links.add(clean_link)
            elif parsed_link.netloc and parsed_link.netloc != start_netloc:
                # External link
                clean_ext_link = parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path
                external_links.add(clean_ext_link)
        site_map.append(url)
        for link in links:
            crawl(link)
    except Exception as e:
        pass  # Ignore errors for robustness

def parse_sitemap(base_url):
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        resp = requests.get(sitemap_url, timeout=10)
        if resp.status_code == 200:
            tree = ET.fromstring(resp.content)
            for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None:
                    parsed = urlparse(loc.text)
                    if parsed.netloc == urlparse(base_url).netloc:
                        clean_url = parsed.scheme + '://' + parsed.netloc + parsed.path
                        extra_internal_urls.add(clean_url)
    except Exception:
        pass

def parse_robots(base_url):
    robots_url = urljoin(base_url, '/robots.txt')
    try:
        resp = requests.get(robots_url, timeout=10)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                if line.lower().startswith('disallow:') or line.lower().startswith('allow:'):
                    path = line.split(':', 1)[1].strip()
                    if path and not path.startswith('#'):
                        full_url = urljoin(base_url, path)
                        parsed = urlparse(full_url)
                        if parsed.netloc == urlparse(base_url).netloc:
                            clean_url = parsed.scheme + '://' + parsed.netloc + parsed.path
                            extra_internal_urls.add(clean_url)
    except Exception:
        pass

if __name__ == "__main__":
    # Parse sitemap.xml and robots.txt for extra internal URLs
    parse_sitemap(START_URL)
    parse_robots(START_URL)
    # Crawl starting URL and all discovered extra internal URLs
    crawl(START_URL)
    for url in extra_internal_urls:
        crawl(url)
    print("Site Map:")
    for link in site_map:
        print(link)
    print("\nExternal Links:")
    for ext_link in sorted(external_links):
        print(ext_link)
    # Find unlinked internal pages (including those from sitemap/robots)
    all_discovered_internal = all_internal_links | extra_internal_urls
    unlinked_internal_pages = sorted(all_discovered_internal - linked_internal_links)
    if unlinked_internal_pages:
        print("\nUnlinked Internal Pages:")
        for page in unlinked_internal_pages:
            print(page)