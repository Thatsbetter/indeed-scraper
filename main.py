import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from proxy import Proxy


def does_it_connect_to_indeed(browser):
    browser.get("http://de.indeed.com/?r=us")
    if "job" in browser.title.lower():
        return True
    else:
        return False


def validate_proxy(proxy_link):
    """Check if the proxy works for Indeed."""
    try:
        with initialize_browser(proxy_link) as browser:
            browser.set_page_load_timeout(5)
            return does_it_connect_to_indeed(browser)
    except:
        return False


def get_indeed_proxies():
    indeed_proxies = []
    connected_proxies = Proxy().get_http_and_false_ssl()[:25]
    for connect in connected_proxies:
        proxy_link = f"{connect['ip']}:{connect['port']}"
        if validate_proxy(proxy_link):
            indeed_proxies.append(proxy_link)
        if len(indeed_proxies) > 5:
            break

    if indeed_proxies:
        return indeed_proxies
    else:
        print("No proxies found.")
        time.sleep(400)
        return get_indeed_proxies()


def initialize_browser(proxy_link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--proxy-server=http://{}'.format(proxy_link))
    options.add_argument("--window-size=1280,700")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return browser


def get_job_links(skill, place, browser, page=1):
    job_links = []
    skill = skill.replace(' ', '+')
    url = f"http://de.indeed.com/jobs?q={skill}&l={place}&fromage=14&start={page * 10}"
    try:
        browser.get(url)
        time.sleep(5)
        browser.save_screenshot(f"indeed_{page}.png")
        # WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tapItem')))
        jobs = browser.find_elements(By.CLASS_NAME, 'tapItem')
        for job in jobs:
            job_link_element = job.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle')
            job_link = job_link_element.get_attribute('href')
            job_links.append(job_link)
    except Exception as e:
        print(f"Error loading page: {str(e)}")
    return job_links


def scrape_job_details(browser, job_links, home_office_keyword, job_requirements_keyword):
    for link in job_links:
        try:
            browser.get(link)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.jobsearch-JobInfoHeader-title span')))
            job_title_element = browser.find_element(By.CSS_SELECTOR, 'h1.jobsearch-JobInfoHeader-title span')
            job_title = job_title_element.text.strip()
            job_desc_div = browser.find_element(By.ID, "jobDescriptionText")
            text_content = job_desc_div.get_attribute('innerText').strip()

            if (any(keyword in text_content for keyword in home_office_keyword) and
                    any(keyword in text_content for keyword in job_requirements_keyword)):
                print(f"Job Title: {job_title}")
                print(f"Job Link: {link}")
                print("--------------------------------------------------------")

        except Exception as e:
            print(f"Error processing job: {e}")


def main():
    home_office_keyword = ['home based working', 'home based', 'homebased', 'remote working', 'remote environment',
                           'remote office', 'home office team', 'home-based team', 'homebased opportunity',
                           'homeoffice',
                           'home based worker', 'remote team', 'homebased job', 'home based position',
                           'home-based environment', 'home-based employee', 'home-based position', 'home office',
                           'home-based job', 'remote employee', 'homebased', 'home based work', 'home office work',
                           'remote', 'home office opportunity', 'homebased working', 'home office position',
                           'remote work', 'homebased worker', 'home-based work', 'telecommute', 'home office worker',
                           'home based ', 'work from home', 'home-based working', 'home office ',
                           'home-based', 'home based environment', 'home-office', 'homebased position',
                           'home office ', 'home based', 'remote', 'homebased employee', 'remote job',
                           'home based job', 'remote position', 'home-based', 'homebased team', 'remote opportunity',
                           'homeoffice job', 'home based employee', 'remote worker', 'home office',
                           'homebased environment', 'homebased work', 'home based team', 'home-based worker',
                           'home-based opportunity', 'home office employee']

    job_requirements_keyword = ["wirtschaftsinginieur", "wirtschaftsingenieurwesen", "wirtschaftsingenieur",
                                "wirtschaftsingenieurin", "projektmanagement", "projektmanager",
                                "projektmanagerin", "projektmanagement", "project management", "project manager",
                                "Nachhaltigkeit", "nachhaltigkeitsmanagement", "projektmanagement", "projektmanager",
                                "projektmanagerin", "manager", "management", "sustainability",
                                "renewable energy", "solar", "green operations", "green energy", "solar energy"]

    skills = [
        "sustainability consultant",
        "sustainability manager",
        "sustainability coordinator",
        "sustainable development",
        "renewable energy",
        "sustainable manufacturing",
        "green operations",
        "industrial sustainability",
        "environmental engineer",
        "project manager solar"
    ]
    places = ["hamburg", "deutschland"]

    proxy_list = get_indeed_proxies()
    print(f"Found {len(proxy_list)} working proxies.")
    job_links = []
    for skill in skills:
        for place in places:
            time.sleep(5)
            for page in range(1, 5):
                with initialize_browser(random.choice(proxy_list)) as browser:
                    job_links = get_job_links(skill, place, browser, page)
                print(f"Found {len(job_links)} job links.")
    for job_link in job_links:
        with initialize_browser(random.choice(proxy_list)) as browser:
            scrape_job_details(browser, job_link, home_office_keyword, job_requirements_keyword)


if __name__ == "__main__":
    main()
