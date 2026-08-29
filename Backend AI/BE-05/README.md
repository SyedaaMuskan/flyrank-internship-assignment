# The Polite Scraper

## Target Classification

### Target
This project scrapes the public practice website Books to Scrape:

https://books.toscrape.com/

### Why this target?
Books to Scrape is a sandbox designed specifically for practicing web scraping. It is appropriate for this educational assignment because the site exists for scraping practice.

### Scope
This scraper will only process the first three catalogue pages, discovering and collecting information from 60 book pages.

### Data collected
For each book, the scraper will collect:

- Title
- Product URL
- Price text
- Availability text
- Rating text
- Description
- Source page
- Fetch timestamp

### Robots.txt check
I requested:

https://books.toscrape.com/robots.txt

The server returned HTTP status code 404, so no robots file was found.

A missing robots.txt file is not permission to scrape a website. It only means that no robots.txt file was available at that location.

### Ethical commitment
I will not reuse this code on another site without checking its rules and terms first.