import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime
import time

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

    def scrape_page(self, url: str, callback: Optional[Callable] = None) -> List[Dict[str, str]]:
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
                
                # Call the callback function if provided
                if callback:
                    callback(business_data)

        return results

    def save_to_excel(self, data: List[Dict[str, str]], filename: str):
        """Save the scraped data to an Excel file inside 'Just Data' folder."""
        try:
            # Get the absolute path of the current script
            base_dir = os.path.abspath(os.path.dirname(__file__))
            data_dir = os.path.join(base_dir, 'Just Data')
            
            # Ensure the directory exists
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            file_path = os.path.join(data_dir, filename)
            df = pd.DataFrame(data)
            
            # Create Excel writer with xlsxwriter engine
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='JustDial Data')
                
                # Auto-adjust column widths
                worksheet = writer.sheets['JustDial Data']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
            
            logging.info(f"Data saved to {file_path}")
            return file_path
            
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")
            raise

    def scrape_multiple_pages(self, base_url: str, start_page: int = 1, end_page: int = 20, callback: Optional[Callable] = None):
        """Scrape multiple pages from JustDial."""
        all_data = []
        try:
            for page in range(start_page, end_page + 1):
                url = f"{base_url}/page-{page}"
                logging.info(f"Scraping page {page} of {end_page}")
                
                # Scrape the page and get data
                page_data = self.scrape_page(url)
                all_data.extend(page_data)
                
                # Call callback with current progress if provided
                if callback:
                    callback({
                        'current_page': page,
                        'total_pages': end_page,
                        'page_data': page_data,
                        'total_records': len(all_data)
                    })
                
                # Add a small delay between pages
                time.sleep(2)

            # Save final results only once
            if all_data:
                filename = f"justdial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                return self.save_to_excel(all_data, filename)
            
        except Exception as e:
            logging.error(f"Error during multi-page scraping: {e}")
            # Save partial data if we have any
            if all_data:
                filename = f"partial_justdial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                return self.save_to_excel(all_data, filename)
            raise


def main():
    base_url = "https://www.justdial.com/Ernakulam/Schools-in-Kureekad/nct-10422444"
    scraper = JustDialScraper()
    
    try:
        scraper.scrape_multiple_pages(base_url, start_page=1, end_page=40)
    except Exception as e:
        logging.error(f"Error occurred during scraping: {e}")
        logging.info("Saving whatever data has been scraped so far.")
        # Save whatever data has been scraped up until the point of failure
        filename = f"partial_hotels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        scraper.save_to_excel([], filename)

if __name__ == "__main__":
    main()
