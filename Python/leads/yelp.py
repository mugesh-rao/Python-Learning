import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import random

class YelpScraper:
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Ensure the 'Yelp Data' folder exists
        if not os.path.exists('Yelp Data'):
            os.makedirs('Yelp Data')

    def extract_name(self, element) -> str:
        try:
            name_element = element.find('a', {'class': 'css-1egxyvc'})
            return name_element.text.strip() if name_element else "Name not found"
        except Exception as e:
            logging.error(f"Error extracting name: {e}")
            return "Error extracting name"

    def extract_phone(self, element) -> str:
        try:
            phone_element = element.find('p', {'class': 'css-1p9ibgf'})
            return phone_element.text.strip() if phone_element else "Phone not found"
        except Exception as e:
            logging.error(f"Error extracting phone: {e}")
            return "Phone not found"

    def extract_rating(self, element) -> str:
        try:
            rating_element = element.find('div', {'role': 'img'})
            return rating_element['aria-label'].replace(" star rating", "") if rating_element else "N/A"
        except Exception as e:
            logging.error(f"Error extracting rating: {e}")
            return "N/A"

    def extract_reviews(self, element) -> str:
        try:
            review_element = element.find('span', {'class': 'css-chan6m'})
            return review_element.text.strip() if review_element else "0 reviews"
        except Exception as e:
            logging.error(f"Error extracting reviews: {e}")
            return "0 reviews"

    def scrape_page(self, url: str):
        """Scrape a single Yelp search results page."""
        logging.info(f"🔍 Fetching: {url}")
        response = self.session.get(url)

        if response.status_code != 200:
            logging.error(f"❌ Failed to fetch {url} (Status Code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', {'class': 'container__09f24__'})
        results = []

        for listing in listings:
            business_data = {
                'Name': self.extract_name(listing),
                'Phone': self.extract_phone(listing),
                'Rating': self.extract_rating(listing),
                'Reviews': self.extract_reviews(listing)
            }
            results.append(business_data)
            logging.info(f"✅ Scraped: {business_data['Name']} - {business_data['Rating']} stars - {business_data['Reviews']}")

        return results

    def save_to_excel(self, data):
        """Save the scraped data to an Excel file inside 'Yelp Data' folder."""
        if not data:
            logging.warning("⚠️ No data to save.")
            return

        filename = f"yelp_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join('Yelp Data', filename)
        df = pd.DataFrame(data)

        try:
            df.to_excel(file_path, index=False, sheet_name='Yelp Data')
            logging.info(f"💾 Data saved to {file_path}")
        except Exception as e:
            logging.error(f"❌ Error saving to Excel: {e}")

def main():
    url = "https://www.yelp.com/search?find_desc=Car+Dealers&find_loc=San+Francisco%2C+CA"
    scraper = YelpScraper()

    data = scraper.scrape_page(url)
    scraper.save_to_excel(data)

if __name__ == "__main__":
    main()
