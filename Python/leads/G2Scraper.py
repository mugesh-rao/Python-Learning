import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class G2Scraper:
    def __init__(self):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Ensure the 'G2 Data' folder exists
        if not os.path.exists('G2 Data'):
            os.makedirs('G2 Data')

    def extract_company_info(self, url: str) -> Dict[str, str]:
        """Extract company information from G2 profile page."""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            company_data = {
                'Company Name': '',
                'Category': '',
                'Website': '',
                'Description': '',
                'Founded': '',
                'Company Size': '',
                'Rating': '',
                'Total Reviews': '',
                'URL': url
            }
            
            # Extract company name
            try:
                company_data['Company Name'] = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-head__title'))
                ).text.strip()
            except:
                logging.warning("Could not find company name")

            # Extract category
            try:
                company_data['Category'] = self.driver.find_element(
                    By.CSS_SELECTOR, '.product-head__categories'
                ).text.strip()
            except:
                logging.warning("Could not find category")

            # Extract rating
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, '.rating-average')
                company_data['Rating'] = rating_elem.text.strip()
            except:
                logging.warning("Could not find rating")

            # Extract total reviews
            try:
                reviews_elem = self.driver.find_element(By.CSS_SELECTOR, '.review-count')
                company_data['Total Reviews'] = reviews_elem.text.strip()
            except:
                logging.warning("Could not find total reviews")

            # Extract company details
            try:
                details = self.driver.find_elements(By.CSS_SELECTOR, '.product-info__item')
                for detail in details:
                    label = detail.find_element(By.CSS_SELECTOR, '.product-info__label').text.strip()
                    value = detail.find_element(By.CSS_SELECTOR, '.product-info__value').text.strip()
                    
                    if 'Website' in label:
                        company_data['Website'] = value
                    elif 'Founded' in label:
                        company_data['Founded'] = value
                    elif 'Size' in label:
                        company_data['Company Size'] = value
            except:
                logging.warning("Could not find some company details")

            return company_data
            
        except Exception as e:
            logging.error(f"Error extracting company info: {e}")
            return company_data

    def extract_reviews(self, url: str, max_reviews: int = 100) -> List[Dict[str, str]]:
        """Extract reviews from G2 profile page."""
        reviews = []
        try:
            reviews_url = f"{url}/reviews"
            self.driver.get(reviews_url)
            time.sleep(3)

            # Scroll to load more reviews
            reviews_loaded = 0
            while reviews_loaded < max_reviews:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                review_elements = self.driver.find_elements(By.CSS_SELECTOR, '.review')
                if len(review_elements) <= reviews_loaded:
                    break
                
                for review in review_elements[reviews_loaded:]:
                    try:
                        review_data = {
                            'Reviewer': '',
                            'Rating': '',
                            'Date': '',
                            'Title': '',
                            'Content': '',
                            'Pros': '',
                            'Cons': ''
                        }
                        
                        # Extract reviewer name
                        try:
                            review_data['Reviewer'] = review.find_element(
                                By.CSS_SELECTOR, '.reviewer-name'
                            ).text.strip()
                        except:
                            pass

                        # Extract rating
                        try:
                            rating_elem = review.find_element(By.CSS_SELECTOR, '.review-stars')
                            review_data['Rating'] = rating_elem.get_attribute('data-rating')
                        except:
                            pass

                        # Extract review date
                        try:
                            review_data['Date'] = review.find_element(
                                By.CSS_SELECTOR, '.review-date'
                            ).text.strip()
                        except:
                            pass

                        # Extract review title
                        try:
                            review_data['Title'] = review.find_element(
                                By.CSS_SELECTOR, '.review-title'
                            ).text.strip()
                        except:
                            pass

                        # Extract review content
                        try:
                            review_data['Content'] = review.find_element(
                                By.CSS_SELECTOR, '.review-content'
                            ).text.strip()
                        except:
                            pass

                        # Extract pros and cons
                        try:
                            pros = review.find_element(By.CSS_SELECTOR, '.pros-content').text.strip()
                            cons = review.find_element(By.CSS_SELECTOR, '.cons-content').text.strip()
                            review_data['Pros'] = pros
                            review_data['Cons'] = cons
                        except:
                            pass

                        reviews.append(review_data)
                        reviews_loaded += 1
                        
                        if reviews_loaded >= max_reviews:
                            break
                            
                    except Exception as e:
                        logging.error(f"Error extracting review: {e}")
                        continue

            return reviews
            
        except Exception as e:
            logging.error(f"Error extracting reviews: {e}")
            return reviews

    def save_to_excel(self, company_data: Dict[str, str], reviews: List[Dict[str, str]], filename: Optional[str] = None):
        """Save scraped data to Excel file."""
        try:
            if not filename:
                company_name = company_data['Company Name'].lower().replace(' ', '_')
                filename = f"g2_data_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            base_dir = os.path.abspath(os.path.dirname(__file__))
            data_dir = os.path.join(base_dir, 'G2 Data')
            
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            file_path = os.path.join(data_dir, filename)
            
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Save company info
                company_df = pd.DataFrame([company_data])
                company_df.to_excel(writer, sheet_name='Company Info', index=False)
                
                # Save reviews
                if reviews:
                    reviews_df = pd.DataFrame(reviews)
                    reviews_df.to_excel(writer, sheet_name='Reviews', index=False)
                
                # Auto-adjust columns width
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(worksheet.columns):
                        max_length = max(
                            len(str(cell.value)) for cell in col if cell.value
                        )
                        worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2

            logging.info(f"Data saved to {file_path}")
            return file_path
            
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")
            raise

    def scrape_g2_profile(self, url: str, max_reviews: int = 100):
        """Main method to scrape G2 profile."""
        try:
            # Extract company information
            logging.info("Extracting company information...")
            company_data = self.extract_company_info(url)
            
            # Extract reviews
            logging.info("Extracting reviews...")
            reviews = self.extract_reviews(url, max_reviews)
            
            # Save data to Excel
            logging.info("Saving data to Excel...")
            file_path = self.save_to_excel(company_data, reviews)
            
            return file_path
            
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            raise
        finally:
            self.driver.quit()

def main():
    # Example usage
    g2_url = "https://www.g2.com/products/notion/reviews"  # Replace with actual G2 URL
    scraper = G2Scraper()
    
    try:
        file_path = scraper.scrape_g2_profile(g2_url, max_reviews=100)
        print(f"Scraping completed. Data saved to: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 