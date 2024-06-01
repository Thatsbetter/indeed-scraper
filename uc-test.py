import undetected_chromedriver as uc
import time
options = uc.ChromeOptions()
options.headless = True
browser = uc.Chrome(options=options)

from selenium_profiles.webdriver import profiles as profile_manager
from selenium_profiles.profiles import profiles

profile = profiles.Android()  # or .Android()
browser.profiles = profile_manager(driver=browser, profile=profile)
browser.profiles.apply(profile)
time.sleep(5)
browser.minimize_window()
browser.get('https://indeed.com')
browser.maximize_window()
browser.save_screenshot("indeed.png")
print(browser.title)
browser.close()
browser.quit()
