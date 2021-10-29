import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_url(page):
    template = 'https://www.zillow.com/homes/New-York,-NY_rb/{}_p'
    url = template.format(page)
    return url


def get_record(result):

    try:
        price = result.find('div', 'list-card-price').text
    except:
        price = "NAN"

    temp = []
    try:
        ul = result.find('ul', 'list-card-details')
        for li in ul.findAll('li'):
            temp.append(li.text.strip(' ')[0])
        numberOfBedroom = temp[0]
        numberOfBath = temp[1]
        size = temp[2]
        homeType = temp[3]
    except:
        numberOfBedroom = "NAN"
        numberOfBath = "NAN"
        size = "NAN"
        homeType = "NAN"

    try:
        address = result.find('address').text
    except:
        address = 'NAN'

    try:
        date = result.find('div', 'topleft').text
    except:
        date = 'NAN'

    today = datetime.today().strftime('%Y-%m-%d')
    record = price, numberOfBedroom, numberOfBath, size, homeType, address, date, today

    return record


def scroll_down_page(driver, speed=10):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= 6577:
        print('scrolling ...')
        current_scroll_position += speed
        print(current_scroll_position)
        driver.execute_script(
            "window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def main():
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Price', '# Bedroom', '# Bathroom',
                            'size(square feet)', 'homeType', 'address', 'Date', 'Today'])
    for i in range(1, 20):
        browser = webdriver.Chrome(executable_path="./chromedriver")
        print('page:', i)
        url = get_url(i)
        browser.get(url)
        scroll_down_page(browser)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        results = soup.find_all('div', {"class": "list-card-info"})
        
        records = []

        for result in results:
            if result is None:
                pass
            else:
                records.append(get_record(result))
        time.sleep(0.5)
        browser.close()

        # save the job data
        with open('results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(records)

main()
