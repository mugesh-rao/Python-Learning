import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os

# Function to scrape quizzes for each month
def scrape_quizzes_for_month(month):
    
    year = 2021
    base_url = f'https://www.gktoday.in/quizbase/current-affairs-quiz-{month}-{year}?pageno='
    quiz_data = []

    # Start with the first page
    page_num = 1

    while True:
        # Construct the full URL for the current page
        url = f'{base_url}{page_num}'
        
        # Send an HTTP request to fetch the webpage content
        response = requests.get(url)
        
        if response.status_code != 200:  # If the page is not found or there's an error, stop
            break
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all quiz question blocks
        quiz_blocks = soup.find_all('div', class_='sques_quiz')
        
        if not quiz_blocks:  # If no quiz blocks are found, stop scraping
            break
        
        # Loop through each quiz block to extract the question, options, and answer
        for block in quiz_blocks:
            # Extract the question
            question = block.find('div', class_='wp_quiz_question').text.strip()
            question = ' '.join(question.split()[1:]).strip()
            
            # Extract the options (which are in one string)
            options_str = block.find('div', class_='wp_quiz_question_options').text.strip()
            
            # Split options into individual parts
            options = options_str.split('[')
            options = [option.replace(']', '').strip()[1:].strip() for option in options if option.strip()]
            
            # Ensure there are exactly 4 options
            if len(options) == 4:
                option_A, option_B, option_C, option_D = options
            else:
                # Handle cases where there may be fewer options
                option_A, option_B, option_C, option_D = [None] * 4
            
            # Extract the correct answer and explanation
            answer_block = block.find('div', class_='wp_basic_quiz_answer')
            correct_answer = answer_block.find('b').next_sibling.strip().split(' ')[0]
            explanation = answer_block.find('div', class_='answer_hint').text.strip()
            
            # Remove 'Notes:' if it's at the beginning of the explanation
            if explanation.lower().startswith('notes:'):
                explanation = ' '.join(explanation.split()[1:]).strip()
            
            quiz_data.append({
                'Quiz_ID': len(quiz_data) + 1,
                'Question': question,
                'Option_1': option_A,
                'Option_2': option_B,
                'Option_3': option_C,
                'Option_4': option_D,
                'correctAnswer': correct_answer,
                'explanation': explanation
            })
        
        # Move to the next page
        page_num += 1

    # Save the scraped data as an Excel file
    df = pd.DataFrame(quiz_data)

    # Check if the file exists and create a new name if needed
    file_name = f'CA_{month}_{year}.xlsx'
    file_count = 1
    while os.path.exists(file_name):
        file_name = f'CA_{month}_{year}_{file_count}.xlsx'
        file_count += 1

    # Export the data to an Excel file
    df.to_excel(file_name, index=False)
    print(f"Data for {month.capitalize()} scraped and exported to '{file_name}' successfully.")

# List of months in the year in lowercase
months = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]

# Scrape data for each month
for month in months:
    scrape_quizzes_for_month(month)
