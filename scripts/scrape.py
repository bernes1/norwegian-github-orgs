from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

driver = webdriver.Chrome()

driver.set_window_size(1920,1080)

orgs = []

pages = 100

for pagenumber in range(1, pages + 1):
    driver.get(f'https://github.com/search?q=location%3ANorway+repos%3A%3E1+type%3Aorg&type=users&p={pagenumber}')
    elements = driver.find_elements (By.CSS_SELECTOR, ".Text-sc-17v1xeu-0.kulXsl")
    for element in elements:
        print(f"{element.text}")
        orgs.append({"name": element.text})
    print(f"page: {pagenumber}")
    time.sleep(30)

with open("all-github-orgs.json", "w") as file:
    json.dump(orgs, file, indent=4)

driver.quit()