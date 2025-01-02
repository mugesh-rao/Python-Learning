import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
# Base URL of the website
base_url = 'https://www.gktoday.in/quizbase/current-affairs-quiz-december-2024?pageno='

quiz_data = []

url_part = urlparse(base_url).path.split('/')[-1].replace('?pageno=', '')

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

# Convert the data into a pandas DataFrame
df = pd.DataFrame(quiz_data)
file_name = f'{url_part}.xlsx'
df.to_excel(file_name, index=False)
# Export the data to an Excel file
df.to_excel('scraped_quiz_data_separated_options.xlsx', index=False)

print("Data scraped and exported to 'scraped_quiz_data_separated_options.xlsx' successfully.")
