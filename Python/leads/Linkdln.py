import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict

class LinkedInScraper:
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

        # Ensure the 'LinkedIn Data' folder exists
        if not os.path.exists('LinkedIn Data'):
            os.makedirs('LinkedIn Data')

    def extract_name(self, profile) -> str:
        """Extract LinkedIn profile name."""
        try:
            name = profile.find('span', {'class': 'entity-result__title-text'}).text.strip()
            return name
        except Exception as e:
            logging.error(f"Error extracting name: {e}")
            return "Name not found"

    def extract_headline(self, profile) -> str:
        """Extract LinkedIn headline (job title)."""
        try:
            headline = profile.find('div', {'class': 'entity-result__primary-subtitle'}).text.strip()
            return headline
        except Exception as e:
            logging.error(f"Error extracting headline: {e}")
            return "Headline not found"

    def extract_location(self, profile) -> str:
        """Extract location."""
        try:
            location = profile.find('div', {'class': 'entity-result__secondary-subtitle'}).text.strip()
            return location
        except Exception as e:
            logging.error(f"Error extracting location: {e}")
            return "Location not found"

    def extract_connections(self, profile) -> str:
        """Extract connections (if available)."""
        try:
            connections = profile.find('span', {'class': 'entity-result__insights'}).text.strip()
            return connections
        except Exception as e:
            return "Connections not found"

    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """Scrape a single LinkedIn search page."""
        response = self.session.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch {url} (Status Code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        profiles = soup.find_all('div', {'class': 'entity-result__item'})
        results = []

        for profile in profiles:
            name = self.extract_name(profile)
            headline = self.extract_headline(profile)
            location = self.extract_location(profile)
            connections = self.extract_connections(profile)

            data = {
                'Name': name,
                'Headline': headline,
                'Location': location,
                'Connections': connections
            }
            results.append(data)
            logging.info(f"Scraped: {name} - {headline}")

        return results

    def save_to_excel(self, data: List[Dict[str, str]], filename: str):
        """Save scraped data to an Excel file inside 'LinkedIn Data' folder."""
        try:
            file_path = os.path.join('LinkedIn Data', filename)
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")

    def scrape_multiple_pages(self, base_url: str, start_page: int = 1, end_page: int = 5):
        """Scrape multiple LinkedIn pages."""
        all_data = []
        for page in range(start_page, end_page + 1):
            url = f"{base_url}&page={page}"
            logging.info(f"Scraping {url}")
            page_data = self.scrape_page(url)
            all_data.extend(page_data)

            # Dynamically create a filename with timestamp
            filename = f"linkedin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            if all_data:
                self.save_to_excel(all_data, filename)

        logging.info(f"Scraping completed. Data saved to {filename}")

def main():
    base_url = "https://www.linkedin.com/search/results/people/?keywords=software%20developer"
    scraper = LinkedInScraper()

    try:
        scraper.scrape_multiple_pages(base_url, start_page=1, end_page=5)
    except Exception as e:
        logging.error(f"Error occurred during scraping: {e}")
        logging.info("Saving whatever data has been scraped so far.")
        filename = f"partial_linkedin_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        scraper.save_to_excel([], filename)

if __name__ == "__main__":
    main()
