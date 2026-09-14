import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl
from typing import Optional


# =========================
# CONFIGURATION
# =========================

CATALOGUE_URL = "https://books.toscrape.com/"

CACHE_DIR = Path("cache")

CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"

PAGE_2_URL = "https://books.toscrape.com/catalogue/page-2.html"
PAGE_2_CACHE_FILE = CACHE_DIR / "catalogue-page-2.html"

PAGE_3_URL = "https://books.toscrape.com/catalogue/page-3.html"
PAGE_3_CACHE_FILE = CACHE_DIR / "catalogue-page-3.html"

OUTPUT_DIR = Path("output")
BOOKS_FILE = OUTPUT_DIR / "books.json"
ERRORS_FILE = OUTPUT_DIR / "errors.json"

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0"
}

TIMEOUT = 10


# =========================
# PYDANTIC SCHEMA
# =========================

class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str


# =========================
# FETCH CATALOGUE PAGE
# =========================

def fetch_catalogue_page(url, cache_file):

    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")

        print(
            f"CACHE HIT | {url} "
            f"| size={len(html)} bytes"
        )

        return html

    # Politeness delay before every real request
    time.sleep(0.5)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

    except requests.RequestException as error:
        print(f"REQUEST ERROR | {url} | {error}")
        return None

    if response.status_code != 200:
        print(
            f"FETCH FAILED | {url} "
            f"| status={response.status_code}"
        )

        return None

    CACHE_DIR.mkdir(exist_ok=True)

    cache_file.write_text(
        response.text,
        encoding="utf-8"
    )

    print(
        f"FETCH | {url} "
        f"| status={response.status_code} "
        f"| size={len(response.text)} bytes"
    )

    return response.text


# =========================
# DISCOVER BOOK URLS
# =========================

def discover_book_urls(html, source_page):

    soup = BeautifulSoup(html, "html.parser")

    books = soup.select("article.product_pod")

    print(
        f"Books found on {source_page}: "
        f"{len(books)}"
    )

    urls = []

    for book in books:

        link = book.select_one("h3 a")

        if link and link.get("href"):

            url = link.get("href")

            # Resolve relative URL against the
            # catalogue page where it was found.
            url = urljoin(source_page, url)

            print(
                f"Book URL found on {source_page}: "
                f"{url}"
            )

            urls.append(url)

    next_link = soup.select_one("li.next a")

    if next_link and next_link.get("href"):

        next_url = urljoin(
            source_page,
            next_link.get("href")
        )

        print(f"Next URL: {next_url}")

    else:

        print("Next URL: None")

    return urls


# =========================
# FETCH BOOK DETAIL PAGE
# =========================

def fetch_book_page(url, cache_file):

    if cache_file.exists():

        html = cache_file.read_text(
            encoding="utf-8"
        )

        print(
            f"BOOK CACHE HIT | {url} "
            f"| size={len(html)} bytes"
        )

        return html

    # Politeness delay before every real request
    time.sleep(0.5)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

    except requests.RequestException as error:

        print(
            f"BOOK REQUEST ERROR | {url} "
            f"| {error}"
        )

        return None

    if response.status_code != 200:

        print(
            f"BOOK FETCH FAILED | {url} "
            f"| status={response.status_code}"
        )

        return None

    CACHE_DIR.mkdir(exist_ok=True)

    cache_file.write_text(
        response.text,
        encoding="utf-8"
    )

    print(
        f"BOOK FETCH | {url} "
        f"| status={response.status_code} "
        f"| size={len(response.text)} bytes"
    )

    return response.text


# =========================
# PARSE RAW BOOK DETAILS
# =========================

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

    product_area = soup.select_one(
        "div.product_main"
    )

    if not product_area:

        print(
            f"PRODUCT AREA NOT FOUND | "
            f"{product_url}"
        )

        return None

    title_element = product_area.select_one(
        "h1"
    )

    price_element = product_area.select_one(
        "p.price_color"
    )

    availability_element = product_area.select_one(
        "p.instock.availability"
    )

    rating_element = product_area.select_one(
        "p.star-rating"
    )

    description_element = soup.select_one(
        "#product_description + p"
    )

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

    # Extract rating from CSS class
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

    description = (
        description_element.get_text(
            " ",
            strip=True
        )
        if description_element
        else None
    )

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


# =========================
# NORMALIZE PRICE
# =========================

def normalize_price(price_text):

    if not price_text:
        raise ValueError(
            "price_text is missing"
        )

    cleaned = (
        price_text
        .replace("£", "")
        .replace("Â", "")
        .strip()
    )

    try:

        return float(cleaned)

    except ValueError:

        raise ValueError(
            f"Invalid price_text: {price_text}"
        )


# =========================
# NORMALIZE + VALIDATE
# =========================

def normalize_and_validate(
    raw_record
):

    # Make a copy so the original raw
    # record remains unchanged.
    record = raw_record.copy()

    # Convert raw price text into
    # a real number.
    record["price_gbp"] = normalize_price(
        record["price_text"]
    )

    # Validate the complete record
    # against the Pydantic schema.
    validated = BookRecord(**record)

    return validated


# =========================
# SAVE JSON
# =========================

def save_json(file_path, data):

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    # -------------------------
    # 1. Catalogue pages
    # -------------------------

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

    # Each item stores:
    # (book_url, source_page)
    all_book_urls = []

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

    # -------------------------
    # 2. Prepare containers
    # -------------------------

    raw_records = []

    valid_records = []

    errors = []

    # This set makes product_url
    # the identity of a book.
    seen_urls = set()

    # -------------------------
    # 3. Fetch + parse
    # -------------------------

    for index, (
        book_url,
        source_page
    ) in enumerate(
        all_book_urls,
        start=1
    ):

        print(
            f"\nProcessing book "
            f"{index}/{len(all_book_urls)}"
        )

        # Skip duplicate canonical URLs
        if book_url in seen_urls:

            print(
                f"DUPLICATE URL SKIPPED | "
                f"{book_url}"
            )

            continue

        seen_urls.add(book_url)

        book_cache_file = (
            CACHE_DIR
            / f"book-{index:03d}.html"
        )

        book_html = fetch_book_page(
            book_url,
            book_cache_file
        )

        if not book_html:

            errors.append({
                "product_url": book_url,
                "reason": "Failed to fetch detail page"
            })

            continue

        fetched_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        raw_record = parse_book_details(
            book_html,
            book_url,
            source_page,
            fetched_at
        )

        if not raw_record:

            errors.append({
                "product_url": book_url,
                "reason": "Could not parse product details"
            })

            continue

        raw_records.append(
            raw_record
        )

        # -------------------------
        # 4. Normalize + validate
        # -------------------------

        try:

            validated_record = (
                normalize_and_validate(
                    raw_record
                )
            )

            # Convert Pydantic model
            # back to a JSON-compatible dict.
            clean_record = (
                validated_record.model_dump(
                    mode="json"
                )
            )

            valid_records.append(
                clean_record
            )

            print(
                f"VALID RECORD | "
                f"{clean_record['title']} "
                f"| £{clean_record['price_gbp']:.2f}"
            )

        except Exception as error:

            errors.append({
                "product_url": book_url,
                "reason": str(error),
                "record": raw_record
            })

            print(
                f"VALIDATION FAILED | "
                f"{book_url} | {error}"
            )

    # -------------------------
    # 5. Store results
    # -------------------------

    save_json(
        BOOKS_FILE,
        valid_records
    )

    save_json(
        ERRORS_FILE,
        errors
    )

    # -------------------------
    # 6. Checkpoint
    # -------------------------

    print("\n" + "=" * 60)

    print(
        f"detail_pages={len(raw_records)}"
    )

    print(
        f"valid_records={len(valid_records)}"
    )

    print(
        f"errors={len(errors)}"
    )

    print(
        f"unique_urls={len(seen_urls)}"
    )

    print(
        f"\nSaved books to: {BOOKS_FILE}"
    )

    print(
        f"Saved errors to: {ERRORS_FILE}"
    )

    # -------------------------
    # 7. Show first clean record
    # -------------------------

    if valid_records:

        print(
            "\nFIRST VALIDATED RECORD:"
        )

        print(
            json.dumps(
                valid_records[0],
                indent=2,
                ensure_ascii=False
            )
        )