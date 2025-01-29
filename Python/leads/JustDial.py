import requests
from bs4 import BeautifulSoup
import csv
import logging
from typing import Dict, List

class JustDialScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def extract_name(self, element) -> str:
        """Extract business name from the element."""
        try:
            name_element = element.find('div', {'class': 'resultbox_title_anchor'})
            return name_element.text.strip() if name_element else "Name not found"
        except Exception as e:
            logging.error(f"Error extracting name: {e}")
            return "Error extracting name"

    def extract_phone(self, element) -> str:
        """Extract phone number from the element."""
        try:
            call_element = element.find('span', {'class': 'callcontent'})
            return call_element.text.strip() if call_element else "Phone not found"
        except Exception as e:
            logging.error(f"Error extracting phone: {e}")
            return "Error extracting phone"

    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """Scrape a single JustDial page."""
        response = self.session.get(url)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch {url} (Status Code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', {'class': 'resultbox_info'})
        results = []

        for listing in listings:
            business_data = {
                'name': self.extract_name(listing),
                'phone': self.extract_phone(listing)
            }
            results.append(business_data)
            logging.info(f"Scraped: {business_data['name']}")

        return results

    def save_to_csv(self, data: List[Dict[str, str]], filename: str = "hotels.csv"):
        """Save the scraped data to a CSV file."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'phone'])
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")

    def scrape_multiple_pages(self, base_url: str, start_page: int = 1, end_page: int = 20):
        """Scrape multiple pages from JustDial."""
        all_data = []
        for page in range(start_page, end_page + 1):
            url = f"{base_url}/page-{page}"
            logging.info(f"Scraping {url}")
            page_data = self.scrape_page(url)
            all_data.extend(page_data)

        self.save_to_csv(all_data)


def main():
    base_url = "https://www.justdial.com/Chennai/Hotels/nct-10255012"
    scraper = JustDialScraper()
    scraper.scrape_multiple_pages(base_url, start_page=1, end_page=20)

if __name__ == "__main__":
    main()
