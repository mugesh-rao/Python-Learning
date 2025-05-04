import os
import requests
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List

class InstagramGraphAPIScraper:
    def __init__(self, access_token: str):
        """Initialize Instagram Graph API scraper"""
        self.base_url = "https://graph.instagram.com/v20.0"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        if not os.path.exists('Instagram Data'):
            os.makedirs('Instagram Data')

    def get_profile_data(self) -> Dict:
        """Get profile data, media, and insights using Instagram Graph API"""
        try:
            # Step 1: Get Instagram Business Account ID
            user_url = f"https://graph.facebook.com/v20.0/me?fields=accounts{{instagram_business_account}}&access_token={self.access_token}"
            response = requests.get(user_url, headers=self.headers)
            if response.status_code != 200:
                logging.error(f"Failed to fetch user accounts: {response.status_code} - {response.text}")
                return None
            
            user_data = response.json()
            logging.info(f"User accounts response: {user_data}")
            
            # Extract Instagram Business Account ID
            ig_account = None
            for account in user_data.get('accounts', {}).get('data', []):
                if 'instagram_business_account' in account:
                    ig_account = account['instagram_business_account'].get('id')
                    break
            
            if not ig_account:
                logging.error("No Instagram Business Account found in response")
                return None
            logging.info(f"Found Instagram Business Account ID: {ig_account}")

            # Step 2: Get profile info
            profile_url = f"{self.base_url}/{ig_account}?fields=username,biography,followers_count,follows_count,media_count,name,profile_picture_url,website&access_token={self.access_token}"
            profile_response = requests.get(profile_url, headers=self.headers)
            if profile_response.status_code != 200:
                logging.error(f"Failed to fetch profile: {profile_response.status_code} - {profile_response.text}")
                return None

            profile_data = profile_response.json()
            profile_info = {
                'Username': profile_data.get('username', ''),
                'Full Name': profile_data.get('name', ''),
                'Biography': profile_data.get('biography', ''),
                'External URL': profile_data.get('website', ''),
                'Followers': profile_data.get('followers_count', 0),
                'Following': profile_data.get('follows_count', 0),
                'Posts Count': profile_data.get('media_count', 0),
                'Profile Picture URL': profile_data.get('profile_picture_url', ''),
                'Scraped Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Step 3: Get recent media
            media_url = f"{self.base_url}/{ig_account}/media?fields=id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count&access_token={self.access_token}&limit=12"
            media_response = requests.get(media_url, headers=self.headers)
            if media_response.status_code != 200:
                logging.error(f"Failed to fetch media: {media_response.status_code} - {media_response.text}")
                return profile_info

            media_data = media_response.json().get('data', [])
            posts = []
            for post in media_data:
                post_data = {
                    'Post ID': post.get('id', ''),
                    'Shortcode': post.get('id', '').split('_')[0],
                    'Display URL': post.get('media_url', ''),
                    'Likes': post.get('like_count', 0),
                    'Comments': post.get('comments_count', 0),
                    'Is Video': post.get('media_type', '') == 'VIDEO',
                    'Timestamp': post.get('timestamp', ''),
                    'Caption': post.get('caption', ''),
                    'Post URL': post.get('permalink', '')
                }
                posts.append(post_data)

            profile_info['Recent Posts'] = posts
            return profile_info

        except Exception as e:
            logging.error(f"Error fetching profile data: {e}")
            return None

    def save_to_excel(self, data: Dict, username: str) -> str:
        """Save scraped data to Excel file"""
        try:
            filename = f"instagram_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            data_dir = os.path.join(os.getcwd(), 'Instagram Data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            file_path = os.path.join(data_dir, filename)

            profile_data = {k: v for k, v in data.items() if k != 'Recent Posts'}
            posts_data = data.get('Recent Posts', [])

            profile_df = pd.DataFrame([profile_data])
            posts_df = pd.DataFrame(posts_data)

            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                profile_df.to_excel(writer, sheet_name='Profile Info', index=False)
                if not posts_df.empty:
                    posts_df.to_excel(writer, sheet_name='Recent Posts', index=False)
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(worksheet.columns):
                        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
                        worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

            logging.info(f"Data saved to {file_path}")
            return file_path

        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")
            raise

def main():
    access_token = "YOUR_INSTAGRAM_ACCESS_TOKEN_HERE"  # Replace with your token
    
    try:
        scraper = InstagramGraphAPIScraper(access_token)
        print("Scraping authenticated Instagram professional account")
        
        profile_info = scraper.get_profile_data()
        if not profile_info:
            print("Failed to fetch profile data")
            return

        username = profile_info['Username']
        file_path = scraper.save_to_excel(profile_info, username)
        print(f"\nProfile data saved to: {file_path}")
        
        print("\n=== Profile Summary ===")
        print(f"Username: {profile_info['Username']}")
        print(f"Full Name: {profile_info['Full Name']}")
        print(f"Followers: {profile_info['Followers']:,}")
        print(f"Following: {profile_info['Following']:,}")
        print(f"Posts: {profile_info['Posts Count']:,}")
        print(f"Recent Posts Scraped: {len(profile_info['Recent Posts'])}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()