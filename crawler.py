from selenium import webdriver
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from main.models import Product, Price, Subscriber
from django.utils import timezone
import smtplib
from email.mime.text import MIMEText

class Crawler:
    def __init__(self):
        self.email_id = # YOUR EMAIL ID
        self.email_pw = # YOUR EMAIL PASSWORD

    def crawl(self):
        driver = webdriver.PhantomJS()
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

        now = timezone.now()
        print("="*35)
        print("Start at", now)
        
        product_list = result
        for n, p in product_list.items():
            product, created = Product.objects.get_or_create(
                name = n
            )

            if created:
                print("Create |", n)        
            else:
                try:
                    latest_price = product.price_set.latest('date')
                    latest_date = latest_price.date.date()
                    if latest_date == now.date() and latest_price.price == p:
                        continue
                except:
                    print("Error | latest_price DoesNotExist, Product :", n)


            product.price_set.create(
                date = timezone.now(),
                price = p
            )
            print("Save |", n)
            product.save()

        now = timezone.now()
        print("Done at", now, ",", len(product_list), "items")

    def mailing(self):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.email_id, self.email_pw)

        now = timezone.now()
        subscriber_list = Subscriber.objects.all()
        for s in subscriber_list:
            print("#", s)
            now_price = s.product.price_set.last().price
            if now < s.expiry_date:
                if now_price < s.min_price or s.max_price < now_price:
                    print("send", s)
                    msg = MIMEText('Your subscription {} has reached its target price.'.format(s.product.name))
                    msg['Subject'] = 'Alarm'
                    msg['To'] = s.email
                    smtp.sendmail(self.email_id, s.email, msg.as_string())
                    s.delete()
                else:
                    print("nothing")
            else:
                print("delete", s)
                s.delete()
        
        smtp.quit()
        print("Done Mailing")

if __name__ == '__main__':
    c = Crawler()
    c.crawl()
    c.mailing()