import undetected_chromedriver as uc

driver = uc.Chrome()
driver.get('https://indeed.com')
print(driver.title)
driver.close()
driver.quit()
