import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from credential import Credential
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
firefox_options.add_argument("--start-maximized")


# Path to your ChromeDriver
#executable_path = Credential().get_gecko_path()
browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=firefox_options)


url ="https://duckduckgo.com/?q=indeed+deutschland&t=newext&atb=v276-1&ia=web"
browser.get(url)
print(browser.title)

try:
    time.sleep(10)
    # Find the first organic result
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[6]/div[4]/div/div/div/div/section[1]/ol/li[3]/article/div[2]/h2/a"))
    )

    # Scroll into view if necessary
    browser.execute_script("arguments[0].scrollIntoView();", element)

    # Click the element
    element.click()
    print(browser.title)
    time.sleep(12)

    # additional actions or assertions can be done here before closing the driver

finally:
    # Always close the driver after your actions
    browser.quit()