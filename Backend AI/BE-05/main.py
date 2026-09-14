import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone


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


# --------------------------------------------------
# FETCH CATALOGUE PAGE
# --------------------------------------------------

def fetch_catalogue_page(url, cache_file):

    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")

        print(
            f"CACHE HIT | size={len(html)} bytes"
        )

        return html

    # Politeness delay
    time.sleep(0.5)

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

        print(
            f"FETCH FAILED | status={response.status_code}"
        )

        return None

    CACHE_DIR.mkdir(exist_ok=True)

    cache_file.write_text(
        response.text,
        encoding="utf-8"
    )

    print(
        f"FETCH | status={response.status_code} "
        f"| size={len(response.text)} bytes"
    )

    return response.text


# --------------------------------------------------
# DISCOVER BOOK URLS
# --------------------------------------------------

def discover_book_urls(html, source_page):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    books = soup.select(
        "article.product_pod"
    )

    print(
        f"Books found on {source_page}: {len(books)}"
    )

    urls = []

    for book in books:

        link = book.select_one(
            "h3 a"
        )

        if link and link.get("href"):

            url = link.get("href")

            url = urljoin(
                source_page,
                url
            )

            print(
                f"Book URL found on {source_page}: {url}"
            )

            urls.append(url)

    next_link = soup.select_one(
        "li.next a"
    )

    if next_link and next_link.get("href"):

        next_url = urljoin(
            source_page,
            next_link.get("href")
        )

        print(
            f"Next URL: {next_url}"
        )

    else:

        print("Next URL: None")

    return urls


# --------------------------------------------------
# FETCH BOOK DETAIL PAGE
# --------------------------------------------------

def fetch_book_page(url, cache_file):

    if cache_file.exists():

        html = cache_file.read_text(
            encoding="utf-8"
        )

        print(
            f"BOOK CACHE HIT | size={len(html)} bytes"
        )

        return html

    # Politeness delay
    time.sleep(0.5)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

    except requests.RequestException as error:

        print(
            f"BOOK REQUEST ERROR | {error}"
        )

        return None

    if response.status_code != 200:

        print(
            f"BOOK FETCH FAILED | "
            f"status={response.status_code}"
        )

        return None

    CACHE_DIR.mkdir(exist_ok=True)

    cache_file.write_text(
        response.text,
        encoding="utf-8"
    )

    print(
        f"BOOK FETCH | status={response.status_code} "
        f"| size={len(response.text)} bytes"
    )

    return response.text


# --------------------------------------------------
# PARSE BOOK DETAILS
# --------------------------------------------------

def parse_book_details(
    html,
    product_url,
    source_page,
    fetched_at
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Restrict selectors to the product area
    product_area = soup.select_one(
        "div.product_main"
    )

    if not product_area:

        print(
            f"PRODUCT AREA NOT FOUND | {product_url}"
        )

        return None

    # ------------------------------
    # TITLE
    # ------------------------------

    title_element = product_area.select_one(
        "h1"
    )

    # ------------------------------
    # PRICE
    # ------------------------------

    price_element = product_area.select_one(
        "p.price_color"
    )

    # ------------------------------
    # AVAILABILITY
    # ------------------------------

    availability_element = product_area.select_one(
        "p.instock.availability"
    )

    # ------------------------------
    # RATING
    # ------------------------------

    rating_element = product_area.select_one(
        "p.star-rating"
    )

    # ------------------------------
    # DESCRIPTION
    # ------------------------------

    description_element = soup.select_one(
        "#product_description + p"
    )

    # ------------------------------
    # EXTRACT TEXT
    # ------------------------------

    title = (
        title_element.get_text(strip=True)
        if title_element
        else None
    )

    price_text = (
        price_element.get_text(
            " ",
            strip=True
        )
        if price_element
        else None
    )

    availability_text = (
        availability_element.get_text(
            " ",
            strip=True
        )
        if availability_element
        else None
    )

    # ------------------------------
    # RATING TEXT
    # ------------------------------

    rating_text = None

    if rating_element:

        rating_classes = rating_element.get(
            "class",
            []
        )

        rating_words = [
            rating
            for rating in rating_classes
            if rating != "star-rating"
        ]

        if rating_words:

            rating_text = rating_words[0]

    # ------------------------------
    # DESCRIPTION TEXT
    # ------------------------------

    description = (
        description_element.get_text(
            " ",
            strip=True
        )
        if description_element
        else None
    )

    # ------------------------------
    # RAW RECORD
    # ------------------------------

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    # ----------------------------------------------
    # Catalogue pages
    # ----------------------------------------------

    pages = [
        (
            CATALOGUE_URL,
            CACHE_FILE
        ),
        (
            PAGE_2_URL,
            PAGE_2_CACHE_FILE
        ),
        (
            PAGE_3_URL,
            PAGE_3_CACHE_FILE
        ),
    ]

    # This will store:
    #
    # (book_url, source_page)
    #
    all_book_urls = []

    # ----------------------------------------------
    # STEP 1:
    # Fetch catalogue pages
    # ----------------------------------------------

    for page_url, cache_file in pages:

        html = fetch_catalogue_page(
            page_url,
            cache_file
        )

        if html:

            book_urls = discover_book_urls(
                html,
                page_url
            )

            # Keep URL + source page together
            for book_url in book_urls:

                all_book_urls.append(
                    (
                        book_url,
                        page_url
                    )
                )

            print(
                f"URLs collected from this page: "
                f"{len(book_urls)}"
            )

            print(
                f"Total URLs collected so far: "
                f"{len(all_book_urls)}"
            )

    # ----------------------------------------------
    # STEP 2:
    # Fetch and parse every book
    # ----------------------------------------------

    raw_records = []

    for index, (book_url, source_page) in enumerate(
        all_book_urls,
        start=1
    ):

        print(
            f"\nProcessing book "
            f"{index}/{len(all_book_urls)}"
        )

        # Example:
        # book-001.html
        # book-002.html
        # book-003.html

        book_cache_file = (
            CACHE_DIR /
            f"book-{index:03d}.html"
        )

        # Fetch book HTML
        book_html = fetch_book_page(
            book_url,
            book_cache_file
        )

        if not book_html:

            continue

        # Record when the page was fetched
        fetched_at = datetime.now(
            timezone.utc
        ).isoformat()

        # Extract raw fields
        record = parse_book_details(
            book_html,
            book_url,
            source_page,
            fetched_at
        )

        if record:

            raw_records.append(
                record
            )

    # ----------------------------------------------
    # CHECKPOINT
    # ----------------------------------------------

    print(
        f"\ndetail_pages={len(raw_records)}"
    )

    if raw_records:

        print(
            "\nFIRST RAW RECORD:"
        )

        print(
            raw_records[0]
        )