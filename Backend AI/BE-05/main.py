import requests

ROBOTS_URL = "https://books.toscrape.com/robots.txt"

try:
    response = requests.get(
        ROBOTS_URL,
        timeout=10,
        headers={
            "User-Agent": "FlyRankInternship-A9/1.0"
        }
    )

    print(f"Status Code: {response.status_code}")
    print("\nrobots.txt content:")
    print(response.text)

except requests.RequestException as error:
    print(f"Error checking robots.txt: {error}")