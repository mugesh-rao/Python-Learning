import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import os

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL of the webpage
url = 'https://www.gktoday.in/daily-current-affairs-quiz-january-1-2025/'

# Open the page with Selenium
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust sleep time if necessary

# Get the page source after the JavaScript has rendered the content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()

quiz_data = []

# Extract quiz blocks
quiz_blocks = soup.find_all('div', class_='wp_quiz_question')

# Check if quiz_blocks were found
if not quiz_blocks:
    print("No quiz blocks found. The page might be dynamic or the structure is different than expected.")

# Loop through each quiz block to extract question, options, and answers
for block in quiz_blocks:
    try:
        # Extract question text
        question_div = block.find('div', class_='wp_quiz_question')
        question_text = question_div.text.strip() if question_div else 'No Question Found'

        # Extract options
        options_div = block.find('div', class_='wp_quiz_question_options')
        if options_div:
            options_list = options_div.find_all('br')
            option_A = options_list[0].previous_element.strip() if len(options_list) > 0 else 'No Option A'
            option_B = options_list[1].previous_element.strip() if len(options_list) > 1 else 'No Option B'
            option_C = options_list[2].previous_element.strip() if len(options_list) > 2 else 'No Option C'
            option_D = options_list[3].previous_element.strip() if len(options_list) > 3 else 'No Option D'
        else:
            option_A = option_B = option_C = option_D = 'No Options Found'

        # Extract correct answer
        answer_block = block.find('div', class_='wp_basic_quiz_answer')
        correct_answer = 'No Answer Found'
        if answer_block:
            correct_answer_tag = answer_block.find('b')
            if correct_answer_tag:
                correct_answer = correct_answer_tag.next_sibling.strip().split(' ')[0]  # Extract A/B/C/D

        # Extract explanation
        explanation = ''
        if answer_block:
            explanation_div = answer_block.find('div', class_='answer_hint')
            if explanation_div:
                explanation = explanation_div.text.strip()

        # Store the quiz data
        quiz_data.append({
            'Quiz_ID': len(quiz_data) + 1,
            'Question': question_text,
            'Option_1': option_A,
            'Option_2': option_B,
            'Option_3': option_C,
            'Option_4': option_D,
            'correctAnswer': correct_answer,
            'explanation': explanation
        })

    except Exception as e:
        print(f"Error processing quiz block: {e}")

# Convert data to DataFrame
df = pd.DataFrame(quiz_data)

# Check if file exists and create a new name if needed
file_name = 'gktoday_jan_1_2025_quiz.xlsx'
file_count = 1
while os.path.exists(file_name):
    file_name = f'gktoday_jan_1_2025_quiz_{file_count}.xlsx'
    file_count += 1

# Save to Excel
df.to_excel(file_name, index=False)

print(f"Data scraped and exported to '{file_name}' successfully.")
