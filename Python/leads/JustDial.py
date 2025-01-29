import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime

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

        # Ensure the 'Just Data' folder exists
        if not os.path.exists('Just Data'):
            os.makedirs('Just Data')
        
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
            phone = call_element.text.strip() if call_element else "Phone not found"
            return phone if phone.lower() != "show number" else None  # Ignore "Show Number"
        except Exception as e:
            logging.error(f"Error extracting phone: {e}")
            return None  # Skip this entry

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
            name = self.extract_name(listing)
            phone = self.extract_phone(listing)

            if phone:  # Skip if phone number is "Show Number"
                business_data = {'name': name, 'phone': phone}
                results.append(business_data)
                logging.info(f"Scraped: {business_data['name']}")

        return results

    def save_to_excel(self, data: List[Dict[str, str]], filename: str):
        """Save the scraped data to an Excel file inside 'Just Data' folder."""
        try:
            file_path = os.path.join('Just Data', filename)  # Save inside 'Just Data' folder
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")

    def scrape_multiple_pages(self, base_url: str, start_page: int = 1, end_page: int = 20):
        """Scrape multiple pages from JustDial."""
        all_data = []
        for page in range(start_page, end_page + 1):
            url = f"{base_url}/page-{page}"
            logging.info(f"Scraping {url}")
            page_data = self.scrape_page(url)
            all_data.extend(page_data)

            # Dynamically create a filename with timestamp to avoid permission conflicts
            filename = f"hotels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            if all_data:
                self.save_to_excel(all_data, filename)

        logging.info(f"Scraping completed. Data saved to {filename}")


def main():
    base_url = "https://www.justdial.com/Chennai/Hotels/nct-10255012"
    scraper = JustDialScraper()
    
    try:
        scraper.scrape_multiple_pages(base_url, start_page=1, end_page=20)
    except Exception as e:
        logging.error(f"Error occurred during scraping: {e}")
        logging.info("Saving whatever data has been scraped so far.")
        # Save whatever data has been scraped up until the point of failure
        filename = f"partial_hotels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        scraper.save_to_excel([], filename)

if __name__ == "__main__":
    main()
