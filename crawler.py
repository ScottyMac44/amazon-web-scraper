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

# urls = [
#     'https://www.amazon.com/ACEMAGIC-Windows-Computer-Quad-Core-Processor/dp/B0D97Z5VTL/ref=sr_1_1?crid=2FJS96IS4BFE8&dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzEAuCT9-Dft-6gkLiGtsGRen5k1sN_rL5L357ei7KQcGN6mZtH4zcZ4z_ZA3ifZUGkahdzeaDB0cmi3VBcZYQ7M8zHIvGMbQpvqRfiT1nDAck1rtKwnqvAk8dApK3Cg5Hw6rZpINF572wD63ZTw4acauc6lzpyXruQur_QqkM-nauvCU4BxAQzSqlI7-Di3LGo.YerE9j2UH9Ly8jJolOYuRcsL2iZtU_gzRZOFib_HbU4&dib_tag=se&keywords=laptops&qid=1727905816&sprefix=laptops%2Caps%2C172&sr=8-1&th=1',
#     'https://www.amazon.com/Naclud-Computer-Notebook-i3-5005U-Expandable/dp/B0DDLD2483/ref=sr_1_4?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-4',
#     'https://www.amazon.com/HP-Micro-edge-Microsoft-14-dq0040nr-Snowflake/dp/B0947BJ67M/ref=sr_1_5?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-5',
#     'https://www.amazon.com/A315-24P-R7VH-Display-Quad-Core-Processor-Graphics/dp/B0BS4BP8FB/ref=sr_1_6?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-6',
#     'https://www.amazon.com/HP-Students-Business-Quad-Core-Storage/dp/B0B2D77YB8/ref=sr_1_8?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-8'    
# ]

# for url in urls:
#     time.sleep(1)
#     print(scrape(url))

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
    records = []
    

    # Scroll to the bottom of the page to load more items
    # Add a short delay to let the page load
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    print(results) # as long as I can parse this fucking mess and pull out URLs this will work.
    pass

    for item in results:
        try:
            data = scrape(item)
            records.append(data)
        except Exception as e:
            print(f"Error scraping item: {e}")

    driver.close()

    # Process the records
    df = pd.DataFrame(records, columns=['Listing Title,', 'Rating', 'Price (USD)', 'Brand',
                                        'Model Name', 'Screen Size', 'Color', 'Hard Disk Size',
                                        'CPU Model', 'RAM Memory Installed Size', 'Operating System',
                                        'Special Feature', 'Graphics Card Description', 'URL'
                                        ])
    return df

# def scrape_amazon(search_term):
#     ua = UserAgent()
#     options = Options()
#     options.add_argument(f"user-agent={ua.random}")
#     driver = undetected_chromedriver.Chrome(options=options)
#     url = get_url(search_term)
#     driver.get(url)
#     time.sleep(5)
#     records = []
#     while True:

#         # Scroll to the bottom of the page to load more items
#         # Add a short delay to let the page load
#         time.sleep(5)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         results = soup.find_all('div', {'data-component-type': 's-search-result'})

#         for item in results:
#             try:
#                 data = scrape(item)
#                 records.append(data)
#             except Exception as e:
#                 print(f"Error scraping item: {e}")

#         # Check if there is a "Next" button on the page
#         try:
#             nextButton = driver.find_element(By.XPATH, '//a[text()="Next"]')
#             driver.execute_script("arguments[0].scrollIntoView();", nextButton)
#             WebDriverWait(driver, 10).until(ExpectedConditions.element_to_be_clickable(nextButton))
#             nextButton.click()
#         except NoSuchElementException:
#             print("Breaking as Last page Reached")
#             break

#     driver.close()

#     # Process the records
#     df = pd.DataFrame(records, columns=['Listing Title,', 'Rating', 'Price (USD)', 'Brand',
#                                         'Model Name', 'Screen Size', 'Color', 'Hard Disk Size',
#                                         'CPU Model', 'RAM Memory Installed Size', 'Operating System',
#                                         'Special Feature', 'Graphics Card Description', 'URL'
#                                         ])
#     return df

if __name__ == '__main__':
    df = scrape_amazon(SEARCH_TERM)
    #df.to_excel('output.xlsx', index=False)