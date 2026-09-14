import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
CATALOGUE_URL = "https://books.toscrape.com/"

CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"
PAGE_2_URL = "https://books.toscrape.com/catalogue/page-2.html"

PAGE_2_CACHE_FILE = CACHE_DIR / "catalogue-page-2.html"
PAGE_3_URL = "https://books.toscrape.com/catalogue/page-3.html"

PAGE_3_CACHE_FILE = CACHE_DIR / "catalogue-page-3.html"
HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0"
}

TIMEOUT = 10
def fetch_catalogue_page(url,cache_file):
    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")
        print(f"CACHE HIT | size={len(html)} bytes")
        return html
    time.sleep(0.5)  # to avoid being blocked by the server

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
    )
    except requests.RequestException as error:
        print(f"REQUEST ERROR | {error}")
        return None    


    if response.status_code != 200:
        print(f"FETCH FAILED | status={response.status_code}")
        return None   
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file.write_text(response.text, encoding="utf-8") 
    print(
        f"FETCH | status={response.status_code} "
        f"| size={len(response.text)} bytes"
    ) 
    return response.text  

def discover_book_urls(html, source_page):
    soup = BeautifulSoup(html, "html.parser")
    books = soup.select("article.product_pod")
    print(f"Books found on {source_page}: {len(books)}")
    urls=[]

    for book in books:
        link = book.select_one("h3 a")
        if link and link.get("href"):
            url = link.get("href")
            url = urljoin(CATALOGUE_URL, url)
            print(f"Book URL found on {source_page}: {url}")
            urls.append(url)
    next_link = soup.select_one("li.next a")


    if next_link and next_link.get("href"):
        next_url = urljoin(source_page, next_link.get("href"))
        print(f"Next URL: {next_url}")
    else:
        print("Next URL: None")

    return urls

if __name__ == "__main__":

    pages = [
        (CATALOGUE_URL, CACHE_FILE),
        (PAGE_2_URL, PAGE_2_CACHE_FILE),
        (PAGE_3_URL, PAGE_3_CACHE_FILE),
    ]

    all_book_urls = []

    for page_url, cache_file in pages:

        html = fetch_catalogue_page(page_url, cache_file)

        if html:
            book_urls = discover_book_urls(html, page_url)

            all_book_urls.extend(book_urls)

            print(f"URLs collected from this page: {len(book_urls)}")
            print(f"Total URLs collected so far: {len(all_book_urls)}")
