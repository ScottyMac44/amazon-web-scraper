import requests
import lxml # required for soup parser
from bs4 import BeautifulSoup
import pandas as pd

CUSTOM_HEADERS = {
    'accept-language'   : 'en-US,en;q=0.9',
    'user-agent'        : 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def scrape(url):
    response = requests.get(url, headers=CUSTOM_HEADERS)
    bs = BeautifulSoup(response.text, "lxml")

    title_elem = bs.select_one('#productTitle')
    title = title_elem.text.strip()

    rating_elem = bs.select_one('#acrPopover')
    rating = float(rating_elem.attrs.get('title').replace(' out of 5 stars', ''))

    price_elem = bs.select_one('span.a-price').select_one('span.a-offscreen')
    price = float(price_elem.text.strip().replace('$', ''))


    data_dict = {'Listing Title' : title,
                 'Listing Rating': rating,
                 'Listing Price' : price
                 }

    rows = bs.find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 2:
            key = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            data_dict[key] = value

    data_dict['URL'] = url
    
    return data_dict

if __name__ == '__main__':
    print("Running scraper only with hard-coded URLs")
    urls = [
    'https://www.amazon.com/ACEMAGIC-Windows-Computer-Quad-Core-Processor/dp/B0D97Z5VTL/ref=sr_1_1?crid=2FJS96IS4BFE8&dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzEAuCT9-Dft-6gkLiGtsGRen5k1sN_rL5L357ei7KQcGN6mZtH4zcZ4z_ZA3ifZUGkahdzeaDB0cmi3VBcZYQ7M8zHIvGMbQpvqRfiT1nDAck1rtKwnqvAk8dApK3Cg5Hw6rZpINF572wD63ZTw4acauc6lzpyXruQur_QqkM-nauvCU4BxAQzSqlI7-Di3LGo.YerE9j2UH9Ly8jJolOYuRcsL2iZtU_gzRZOFib_HbU4&dib_tag=se&keywords=laptops&qid=1727905816&sprefix=laptops%2Caps%2C172&sr=8-1&th=1',
    'https://www.amazon.com/Naclud-Computer-Notebook-i3-5005U-Expandable/dp/B0DDLD2483/ref=sr_1_4?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-4',
    'https://www.amazon.com/HP-Micro-edge-Microsoft-14-dq0040nr-Snowflake/dp/B0947BJ67M/ref=sr_1_5?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-5',
    'https://www.amazon.com/A315-24P-R7VH-Display-Quad-Core-Processor-Graphics/dp/B0BS4BP8FB/ref=sr_1_6?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-6',
    'https://www.amazon.com/HP-Students-Business-Quad-Core-Storage/dp/B0B2D77YB8/ref=sr_1_8?dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzHb0vbqV0e7ia5AjmLuOSBSm-J_0zg9SpYSsyD9CLeOxZxudnA-XFIKAX846ytF_8vt9vQL5Ym8EsrjjrtiObOKWSR-bnGWeRWKHh0y_pDeUC7fSFXoQVu1Jgyue58rgNz9XkxuZhInjlWYMzJXhvRp_WHjWcu9u36--m9XEHEaKdfeAzrlmuMGPsjVyWxh9jo.VssJL2meCXnrOldcUSNLizyRNCFvvUi5RH346HMJm8Y&dib_tag=se&keywords=laptops&qid=1727928646&sr=8-8']

    # Get data from each URL
    data_list = []
    for url in urls:
        data = scrape(url)
        data_list.append(data)

    # Process the records 
    df = pd.DataFrame(data_list, columns=['Listing Title', 'Listing Rating', 'Listing Price', 'Brand',
                                        'Model Name', 'Screen Size', 'Color', 'Hard Disk Size',
                                        'CPU Model', 'Ram Memory Installed Size', 'Operating System',
                                        'Special Feature', 'Graphics Card Description', 'URL'
                                        ])
    df.to_excel('output.xlsx', index=False)