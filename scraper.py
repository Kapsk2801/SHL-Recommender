import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.shl.com/solutions/products/product-catalog/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}


def scrape():
    response = requests.get(URL, headers=HEADERS)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Failed to fetch")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    assessments = []

    links = soup.find_all("a")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        if title and href:
            if "/products/" in href:
                full_url = href if href.startswith("http") else "https://www.shl.com" + href

                assessments.append({
                    "name": title,
                    "url": full_url
                })

    unique = []
    seen = set()

    for item in assessments:
        if item["url"] not in seen:
            unique.append(item)
            seen.add(item["url"])

    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2)

    print("Saved", len(unique), "assessments")


scrape()