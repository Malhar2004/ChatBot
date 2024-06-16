import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import re



from django.conf import settings

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

# URLs of the pages you want to extract text from
urls = [
    'https://www.stvincentngp.edu.in/',
    'https://www.stvincentngp.edu.in/pages/about-us',
    'https://www.stvincentngp.edu.in/admissions',
    'https://www.stvincentngp.edu.in/training-placements',
    'https://www.stvincentngp.edu.in/pages/naac-grade',
    'https://www.stvincentngp.edu.in/pages/nba-accreditation',
    'https://www.stvincentngp.edu.in/programs/first-year',
    'https://www.stvincentngp.edu.in/programs/civil-engineering',
    'https://www.stvincentngp.edu.in/programs/computer-engineering',
    'https://www.stvincentngp.edu.in/programs/electronics-telecommunication',
    'https://www.stvincentngp.edu.in/programs/electrical-engineering',
    'https://www.stvincentngp.edu.in/programs/information-technology',
    'https://www.stvincentngp.edu.in/programs/mechanical-engineering',
    'https://www.stvincentngp.edu.in/programs/artificial-intelligence',
    'https://www.stvincentngp.edu.in/programs/data-science',
    'https://www.stvincentngp.edu.in/programs/cyber-security',
    'https://www.stvincentngp.edu.in/programs/industrial-IOT',
    'https://www.stvincentngp.edu.in/programs/computer-science-and-business-systems',
    'https://www.stvincentngp.edu.in/pages/academic-cell',
    'https://www.stvincentngp.edu.in/bachelor-of-vocations',
    'https://www.stvincentngp.edu.in/industry-courses',
    'https://www.stvincentngp.edu.in/pages/library',
    'https://www.stvincentngp.edu.in/pages/student-affairs-and-development-cell',
    'https://www.stvincentngp.edu.in/sports',
    'https://www.stvincentngp.edu.in/pages/facility-contact-information',
    'https://www.stvincentngp.edu.in/clubs/view/nss',
    'https://www.stvincentngp.edu.in/clubs/view/rec',
    'https://www.stvincentngp.edu.in/clubs/view/iste',
    'https://www.stvincentngp.edu.in/hostels',
    'https://www.stvincentngp.edu.in/iedcs',
    'https://www.stvincentngp.edu.in/pages/anti-ragging-cell',
    'https://www.stvincentngp.edu.in/pages/womens-grievance-cell',
    'https://www.stvincentngp.edu.in/pages/grievance-redressal-cell',
    'https://www.stvincentngp.edu.in/pages/mou',
    'https://www.stvincentngp.edu.in/pages/m-tech-computer-science-and-engineering',
    'https://www.stvincentngp.edu.in/pages/m-tech-cad-cam',
]

# Additional URLs: Faculties
faculties_list_urls = ['https://www.stvincentngp.edu.in/faculties/list/' + str(i) for i in range(1, 9)]
faculties_view_urls = ['https://www.stvincentngp.edu.in/faculties/view/' + str(i) for i in range(1, 155)]

# Extend the urls list with additional URLs
urls.extend(faculties_list_urls)
urls.extend(faculties_view_urls)

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}

# Function to extract footer content
# Function to extract footer content
def extract_footer(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Try to find footer using specific class or ID
        footer = soup.find('footer', class_='footer-class')  # Update 'footer-class' with actual class if present
        if footer:
            return footer
        footer = soup.find('footer', id='footer-id')  # Update 'footer-id' with actual ID if present
        if footer:
            return footer
        return None
    except Exception as e:
        print(f"Failed to extract footer from {url}: {e}")
        return None

# Function to extract text and remove footer
def extract_text_and_remove_footer(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove footer content
        footer = extract_footer(url)
        if footer:
            footer.decompose()
        # Extract text from the page
        text = soup.get_text()
        # Remove extra newline spaces between paragraphs
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Remove leading and trailing whitespace from each line
        text = '\n'.join(line.strip() for line in text.split('\n'))
        return text
    except Exception as e:
        print(f"Failed to extract text from {url}: {e}")
        return None




# Extract text from each page in parallel
collected_text = ""
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit the tasks for each URL
    tasks = {executor.submit(extract_text_and_remove_footer, url): url for url in urls}
    # Retrieve the results as they become available
    for future in concurrent.futures.as_completed(tasks):
        url = tasks[future]
        text = future.result()
        if text:
            collected_text += f"URL: {url}\n{text}\n\n"

# Writing collected text to a single file
output_file_path = os.path.join(DATA_DIR, 'collected_text.txt')
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(collected_text)
