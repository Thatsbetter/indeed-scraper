import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from credential import Credential
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.options import Options as FireFoxOptions

# Configure Chrome options
firefox_options = FireFoxOptions()
firefox_options.headless = True
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/")
firefox_options.add_argument("--auto-open-devtools-for-tabs")
firefox_options.add_argument("--disable-popup-blocking")


# Path to your ChromeDriver
executable_path = Credential().get_gecko_path()
browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=firefox_options)


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
