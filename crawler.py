# crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
    
# ✅ Extracts internal links (up to max_links)
def extract_internal_links(base_url, max_links=None     ):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(base_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        domain = urlparse(base_url).netloc

        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            if not href:
                continue

            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)

            # Only add same domain internal pages (avoid external or mailto etc.)
            if parsed_url.scheme.startswith("http") and domain in parsed_url.netloc:
                links.add(full_url)

        return list(links)[:max_links]
    except Exception as e:
        print(f"[!] Failed to extract internal links: {e}")
        return []

# ✅ Image URL extractor (your proven working version)
def extract_image_urls(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = [urljoin(url, img.get('src')) for img in img_tags if img.get('src')]
        return image_urls
    except Exception as e:
        print(f"[!] Error extracting images from {url}: {e}")
        return []
