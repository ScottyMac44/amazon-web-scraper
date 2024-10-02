import requests
import lxml # required for soup parser
from bs4 import BeautifulSoup as bs

# url = 'https://www.amazon.com/s?k=laptops&crid=2FJS96IS4BFE8&sprefix=laptops%2Caps%2C172&ref=nb_sb_noss_1'
url = 'https://www.amazon.com/ACEMAGIC-Windows-Computer-Quad-Core-Processor/dp/B0D97Z5VTL/ref=sr_1_1?crid=2FJS96IS4BFE8&dib=eyJ2IjoiMSJ9.HDoVIH6TUTtnZ9iXpSeNZ_EfVIfDd3QL7pzxZjafxzEAuCT9-Dft-6gkLiGtsGRen5k1sN_rL5L357ei7KQcGN6mZtH4zcZ4z_ZA3ifZUGkahdzeaDB0cmi3VBcZYQ7M8zHIvGMbQpvqRfiT1nDAck1rtKwnqvAk8dApK3Cg5Hw6rZpINF572wD63ZTw4acauc6lzpyXruQur_QqkM-nauvCU4BxAQzSqlI7-Di3LGo.YerE9j2UH9Ly8jJolOYuRcsL2iZtU_gzRZOFib_HbU4&dib_tag=se&keywords=laptops&qid=1727905816&sprefix=laptops%2Caps%2C172&sr=8-1&th=1'
custom_headers = {
    'accept-language'   : 'en-US,en;q=0.9',
    'user-agent'        : 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=custom_headers)
# print(response.text)
soup = bs(response.text, "lxml")

title_elem = soup.select_one('#productTitle')
title = title_elem.text.strip()

rating_elem = soup.select_one('#acrPopover')
rating = float(rating_elem.attrs.get('title').replace(' out of 5 stars', ''))

price_elem = soup.select_one('span.a-price').select_one('span.a-offscreen')
price = price_elem.text.strip()

info_table_elem = soup.select_one('table.a-normal').select('td.a-span3')

print(title)
print('-'*40)
print(rating)
print('-'*40)
print(price)
print('-'*40)

print(info_table_elem)