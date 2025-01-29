import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import logging
from typing import Dict, Optional, List

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
            # Look for the title div with specific classes
            name_element = element.find('div', {'class': 'resultbox_title_anchor'})
            if name_element:
                return name_element.text.strip()
            return "Name not found"
        except Exception as e:
            logging.error(f"Error extracting name: {e}")
            return "Error extracting name"

    def extract_phone(self, element) -> str:
        """Extract phone number from the element."""
        try:
            # Look for the call button content
            call_element = element.find('span', {'class': 'callcontent'})
            if call_element:
                return call_element.text.strip()
            return "Phone not found"
        except Exception as e:
            logging.error(f"Error extracting phone: {e}")
            return "Error extracting phone"

    def scrape_page(self, html_content: str) -> List[Dict[str, str]]:
        """Scrape a single page of results."""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Find all business listings
        listings = soup.find_all('div', {'class': 'resultbox_info'})
        
        for listing in listings:
            business_data = {
                'name': self.extract_name(listing),
                'phone': self.extract_phone(listing)
            }
            results.append(business_data)
            logging.info(f"Scraped business: {business_data['name']}")
            
        return results

    def save_to_csv(self, data: List[Dict[str, str]], filename: str = 'contact_details.csv'):
        """Save the scraped data to a CSV file."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'phone'])
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")

def main():
    scraper = JustDialScraper()

    # Fetch HTML content from the JustDial URL
    url = "https://www.justdial.com/Chennai/Hotels/nct-10255012"
    response = scraper.session.get(url)

    if response.status_code == 200:
        results = scraper.scrape_page(response.text)
        scraper.save_to_csv(results, filename="hotels.csv")
    else:
        logging.error(f"Failed to fetch data from {url}. Status code: {response.status_code}")

if __name__ == "__main__":
    main()

if __name__ == '__main__':
    main()