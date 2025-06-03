import asyncio
import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

def extract_tag_contents(url):
    response = scraper.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for unwanted in soup(['script', 'style']):
        unwanted.decompose()

    # Extract and clean text
    text = soup.get_text(separator="\n", strip=True)
    return text

if __name__ == "__main__":
    res = extract_tag_contents("https://www.cnbc.com/2025/05/31/angela-duckworth-how-kids-can-use-ai-to-become-smarter-adults.html")
    print(res)