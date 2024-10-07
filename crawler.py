from scraper import scrape
import time
import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import pandas as pd
import time
from fake_useragent import UserAgent

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# NOTE a lot of this code was taken from this stack overflow question
# https://stackoverflow.com/questions/76302452/how-to-scrape-all-of-the-pages-on-amazon-from-a-search-result-with-python
# learning how to write bot detection avoidance/captcha avoidance is hard

SEARCH_TERM = 'laptops'

def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    return url

def scrape_amazon(search_term):
    ua = UserAgent()
    options = Options()
    options.add_argument(f"user-agent={ua.random}")
    driver = undetected_chromedriver.Chrome(options=options, driver_executable_path=None)
    url = get_url(search_term)
    driver.get(url)
    time.sleep(5)

    itr = 0
    while True:
        itr+=1
        print(f'scraping page {itr}')

        # Scroll to the bottom of the page to load more items
        # Add a short delay to let the page load
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        results_parser = BeautifulSoup(str(results), 'lxml')
        item_links = []

        for a_tag in results_parser.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'):
            href = a_tag.get('href')
            if href and "/dp/" in href:
                item_links.append(href)

        records = []
        link_itr = 0
        for item in item_links:
            link_itr+=1
            try:
                print(f'scraping item {link_itr} on page {itr}')
                data = scrape(f'https://www.amazon.com{item}')
                records.append(data)
            except Exception as e:
                print(f"Error scraping item: {e}")

        df = pd.DataFrame(records, columns=['Listing Title', 'Listing Rating', 'Listing Price', 'Brand',
                                'Model Name', 'Screen Size', 'Color', 'Hard Disk Size',
                                'CPU Model', 'Ram Memory Installed Size', 'Operating System',
                                'Special Feature', 'Graphics Card Description', 'URL'
                                ])
        df.to_excel(f'output{itr}.xlsx', index=False)

        try:
            nextButton = driver.find_element(By.XPATH, '//a[text()="Next"]')
            driver.execute_script("arguments[0].scrollIntoView();", nextButton)
            WebDriverWait(driver, 10).until(ExpectedConditions.element_to_be_clickable(nextButton))
            nextButton.click()
        except NoSuchElementException:
            print("Breaking as Last page Reached")
            break

    driver.close()

if __name__ == '__main__':
    scrape_amazon(SEARCH_TERM)