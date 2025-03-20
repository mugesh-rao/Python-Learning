import requests
import re
import time
import csv

# Populate below list with URLs to be scraped
masterlist = [
    "https://clutch.co/agencies/new-york",
    "https://clutch.co/uk/agencies/creative"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
}

# Decodes obfuscated contact details
def solver(lst, string):
    return "".join([string.split('#')[i] for i in lst if i < len(string.split('#'))])

# Open CSV file for appending data
with open('lst.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Email", "Page URL"])

    for master_url in masterlist:
        init_response = requests.get(master_url, headers=headers)
        if init_response.status_code != 200:
            print(f"Failed to fetch {master_url}")
            continue

        # Extract the number of pages
        max_pages = re.findall(r"<li class=\"pager-current\">1 of (\d+)</li>", init_response.text)
        max_pages = int(max_pages[0]) if max_pages else 1  # Default to 1 if no pages found
        print(f"Scraping {max_pages} pages from {master_url}")

        for p in range(max_pages):  # Start from page 0
            page_url = f"{master_url}?page={p}"
            response = requests.get(page_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch page {p} of {master_url}")
                continue

            # Extract profile URLs
            to_hit = re.findall(r'<a href="(https://clutch.co/profile/[\w\d-]*)" target="_blank">', response.text)

            for brand_url in to_hit:
                response1 = requests.get(brand_url, headers=headers)
                if response1.status_code != 200:
                    print(f"Failed to fetch brand page: {brand_url}")
                    continue

                # Extract email (Improved regex for common email formats)
                emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", response1.text)

                # Extract company name
                names = re.findall(r'<h1[^>]*>(.*?)</h1>', response1.text)
                company_name = names[0].strip() if names else "Unknown"

                # Extract obfuscated phone numbers (if any)
                codes = re.findall(r"document.getElementById\(.*'\).innerHTML = (.*)", response1.text)
                decoded_emails = []

                if emails and codes:
                    for i, code in enumerate(codes):
                        cleaned_code = re.sub("[^0-9]", "", code)  # Keep only numbers
                        index_list = [int(digit) for digit in cleaned_code]  # Convert to list of integers
                        decoded_emails.append(solver(index_list, emails[i]))

                final_emails = decoded_emails if decoded_emails else emails

                if final_emails:
                    for email in final_emails:
                        writer.writerow([company_name, email, page_url])
                        with open('progress.txt', 'a', encoding='utf-8') as prog:
                            prog.write(f"{brand_url} {page_url}\n")
                        print(f"Scraped: {company_name} - {email} from {page_url}")

                else:
                    print(f"No email found for {company_name} on {brand_url}")

                # Avoid excessive requests to prevent blocking
                time.sleep(2)
