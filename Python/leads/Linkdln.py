import os
import requests
import time
import random
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class LinkedInScraper:
    def __init__(self, email: str, password: str):
        """Initialize with LinkedIn credentials"""
        self.email = email
        self.password = password
        
        # Setup Chrome options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Commented out for debugging
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Ensure the 'LinkedIn Data' folder exists
        if not os.path.exists('LinkedIn Data'):
            os.makedirs('LinkedIn Data')
            
        self._login()

    def _login(self):
        """Login to LinkedIn"""
        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)
            
            # Wait for and fill email
            email_elem = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
            email_elem.send_keys(self.email)
            
            # Fill password
            password_elem = self.driver.find_element(By.ID, 'password')
            password_elem.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(3)
            logging.info("Successfully logged in to LinkedIn")
            
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise Exception("Failed to login to LinkedIn")

    def extract_contact_info(self, profile_url: str) -> Dict[str, str]:
        """Extract contact information from a profile."""
        try:
            # Navigate to contact info page
            contact_url = profile_url.replace('/in/', '/in/~/contact-info/')
            self.driver.get(contact_url)
            time.sleep(2)

            contact_info = {
                'Email': 'Not available',
                'Phone': 'Not available',
                'Profile URL': profile_url
            }

            # Try to find email
            try:
                email_section = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "section.ci-email")))
                email = email_section.find_element(By.CSS_SELECTOR, "a").text.strip()
                contact_info['Email'] = email
            except:
                logging.warning(f"No email found for profile: {profile_url}")

            # Try to find phone
            try:
                phone_section = self.driver.find_element(By.CSS_SELECTOR, "section.ci-phone")
                phone = phone_section.find_element(By.CSS_SELECTOR, "span").text.strip()
                contact_info['Phone'] = phone
            except:
                pass

            return contact_info

        except Exception as e:
            logging.error(f"Error extracting contact info: {e}")
            return None

    def scrape_company_employees(self, company_url: str, max_employees: int = 100) -> List[Dict[str, str]]:
        """Scrape employee information from a company page."""
        try:
            # Convert company URL to employees page
            if 'company' in company_url:
                employees_url = f"{company_url}/people/"
            else:
                raise ValueError("Please provide a valid company URL (e.g., https://www.linkedin.com/company/company-name/)")

            self.driver.get(employees_url)
            time.sleep(3)

            employees_data = []
            processed_count = 0

            while processed_count < max_employees:
                # Scroll to load more results
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Find employee profiles
                employee_cards = self.driver.find_elements(By.CSS_SELECTOR, ".org-people-profile-card")

                for card in employee_cards[processed_count:]:
                    try:
                        # Extract basic info
                        name = card.find_element(By.CSS_SELECTOR, ".org-people-profile-card__profile-title").text.strip()
                        title = card.find_element(By.CSS_SELECTOR, ".org-people-profile-card__profile-position").text.strip()
                        
                        # Get profile URL
                        profile_link = card.find_element(By.CSS_SELECTOR, "a.org-people-profile-card__profile-link")
                        profile_url = profile_link.get_attribute("href")

                        # Get contact info
                        contact_info = self.extract_contact_info(profile_url)

                        employee_data = {
                            'Name': name,
                            'Title': title,
                            'Profile URL': profile_url,
                            'Email': contact_info['Email'] if contact_info else 'Not available',
                            'Phone': contact_info['Phone'] if contact_info else 'Not available',
                            'Company URL': company_url,
                            'Scraped Date': datetime.now().strftime('%Y-%m-%d')
                        }

                        employees_data.append(employee_data)
                        processed_count += 1
                        
                        logging.info(f"Scraped: {name} - {employee_data['Email']}")

                        if processed_count >= max_employees:
                            break

                        # Random delay between profiles
                        time.sleep(1 + random.random() * 2)

                    except Exception as e:
                        logging.error(f"Error processing employee card: {e}")
                        continue

            return employees_data

        except Exception as e:
            logging.error(f"Error scraping company employees: {e}")
            return []

    def save_to_excel(self, data: List[Dict[str, str]], company_name: str):
        """Save scraped data to an Excel file."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            folder_path = os.path.join('LinkedIn Data', today)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"linkedin_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = os.path.join(folder_path, filename)
            
            df = pd.DataFrame(data)
            df = df.drop_duplicates(subset=['Email', 'Profile URL'], keep='first')
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Employee Contacts')
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Employee Contacts']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
            
            logging.info(f"Data saved to {file_path}")
            logging.info(f"Total unique profiles: {len(df)}")
            
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")

def main():
    # Add your LinkedIn credentials here
    EMAIL = "nesetha123@gmail.com"
    PASSWORD = "Nesetha@123"
    
    # Company URL to scrape (example: Microsoft's LinkedIn page)
    COMPANY_URL = "https://www.linkedin.com/company/microsoft"
    
    # Extract company name from URL for filename
    company_name = COMPANY_URL.split('company/')[1].replace('/', '')
    
    try:
        scraper = LinkedInScraper(EMAIL, PASSWORD)
        employees_data = scraper.scrape_company_employees(
            company_url=COMPANY_URL,
            max_employees=100  # Adjust this number as needed
        )
        
        if employees_data:
            scraper.save_to_excel(employees_data, company_name)
        else:
            logging.warning("No data was collected during scraping")
            
    except Exception as e:
        logging.error(f"Error occurred during scraping: {e}")
    finally:
        scraper.driver.quit()

if __name__ == "__main__":
    main()
