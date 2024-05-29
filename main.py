import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
browser.get("https://www.google.com")
print(browser.title)

# Define your search parameters
skill = "project manager solar"
place = "hamburg"

keywords = ["home office", "remote work", "telecommute", "work from home", "remote", "home-based", "homebased",
            "home based", "remote job", "remote position", "remote opportunity", "remote role", "remote work",
            "remote working", "remote worker", "remote employee", "remote team", "remote office", "remote environment",
            "homeoffice job", "home office position", "home office opportunity", "home office role", "home office work",
            "home office working", "home office worker", "home office employee", "home office team",
            "home office environment", "home-based job", "home-based position", "home-based opportunity",
            "home-based role", "home-based work", "home-based working", "home-based worker", "home-based employee",
            "home-based team", "home-based environment", "homebased job", "homebased position", "homebased opportunity",
            "homebased role", "homebased work", "homebased working", "homebased worker", "homebased employee",
            "homebased team", "homebased environment", "home based job", "home based position",
            "home based opportunity", "home based role", "home based work", "home based working", "home based worker",
            "home based employee", "home based team", "home based environment", "homeoffice", "home-office"]

url = f"https://de.indeed.com/jobs?q={skill}&l={place}"
browser.get(url)

time.sleep(5)  # Allow some time for the page to load

jobs = browser.find_elements(By.CLASS_NAME, 'tapItem')
job_links = []
for job in jobs:
    try:
        job_link_element = job.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle')
        job_id = job_link_element.get_attribute('id')
        job_link = job_link_element.get_attribute('href')
        job_links.append(job_link)
    except Exception as e:
        print(f"Error processing job: {e}")
print(len(job_links))
for link in job_links:
    try:
        browser.get(link)
        time.sleep(2)
        job_title_element = browser.find_element(By.CSS_SELECTOR, 'h1.jobsearch-JobInfoHeader-title span')
        job_title = job_title_element.text.strip()
        job_desc_div = browser.find_element(By.ID, "jobDescriptionText")
        text_content = job_desc_div.get_attribute('innerText').strip()
        if any(keyword in text_content for keyword in keywords):
            print(f"Job Title: {job_title}")
            print(f"Job Link: {link}")
            print("--------------------------------------------------------")
    except Exception as e:
        print(f"Error processing job: {e}")
browser.close()
browser.quit()
