import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.gktoday.in/page/{}/"

# Define the target date
target_date = "January 2, 2025"

# Prepare a list for storing questions and answers
qa_list = []

# Page counter
page = 1
stop_scraping = False

while not stop_scraping:
    # Fetch the webpage content
    url = base_url.format(page)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch webpage: {response.status_code}")
        break

    # Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the articles
    articles = soup.find_all('h1', id='list')

    for article in articles:
        # Extract the question from the title
        question_tag = article.find('a')
        if question_tag:
            question = question_tag.text.strip()

            # Extract the answer from the following sibling <p>
            answer_tag = article.find_next_sibling('p')
            if answer_tag:
                answer = answer_tag.text.strip()

                # Append to the list
                qa_list.append({"Question": question, "Answer": answer})

    # Check the meta_date for the last entry on the page
    meta_dates = soup.find_all('span', class_='meta_date')
    for meta_date in meta_dates:
        if meta_date.text.strip() == target_date:
            stop_scraping = True
            break

    # Increment the page counter
    page += 1

# Save the data to an Excel file
excel_file = f"{target_date}.xlsx"
df = pd.DataFrame(qa_list)
df.to_excel(excel_file, index=False)

print(f"Scraped {len(qa_list)} questions and answers and saved to {excel_file}.")
