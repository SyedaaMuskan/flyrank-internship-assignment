# Books to Scrape — Polite Book Scraper

A small Python scraper built as part of the FlyRank Backend Engineering internship.

The scraper discovers book detail pages from the Books to Scrape catalogue, fetches the detail pages politely, extracts raw fields, normalizes prices, validates records with Pydantic, handles individual page failures, and writes reproducible JSON output.

## Stage 0 — Target Classification

**Target:** Books to Scrape

**Classification:** Public, static HTML website.

The required book information is already present in the HTML returned by the server, so this scraper does not require browser automation.

## What the scraper does

The pipeline:

1. Fetches catalogue pages.
2. Discovers book detail URLs.
3. Resolves URLs to absolute canonical URLs.
4. Fetches and caches detail pages.
5. Extracts raw book information.
6. Keeps the original `price_text`.
7. Converts `price_text` into numeric `price_gbp`.
8. Validates every record with Pydantic.
9. Sends invalid records to `errors.json`.
10. Deduplicates books using their canonical product URL.
11. Writes valid records to `output/books.json`.
12. Writes run statistics to `output/run-report.json`.

## Lane

**Backend / Python Web Scraping**

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `pydantic`

## Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python -m venv .venv