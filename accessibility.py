import requests
from bs4 import BeautifulSoup

def is_website_accessible(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"[✗] Status code: {response.status_code}")
            return False

        if "text/html" not in response.headers.get("Content-Type", ""):
            print("[✗] Not an HTML page.")
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        if not (soup.find("img") or soup.find("script") or soup.find("link")):
            print("[✗] No useful content to analyze.")
            return False

        return True
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False
