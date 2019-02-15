from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:\\chromedriver')
driver.get('http://prod.danawa.com/list/?cate=112752')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

main_prodlist = soup.find('div', {'class':'main_prodlist'}).find('ul').findAll('li', {'class':'prod_item'})

result = {}

for product in main_prodlist:
    name = product.find('p', {'class':'prod_name'}).find('a').text.lstrip().rstrip()
    price = product.find('p', {'class':'price_sect'}).find('a').text.lstrip().rstrip()
    price = int(price[:-1].replace(',', ''))
    result[name] = price

if __name__ == '__main__':
    print(result)