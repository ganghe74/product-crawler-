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
        self.driver = webdriver.PhantomJS()
        self.email_id = '' # YOUR EMAIL ID
        self.email_pw = '' # YOUR EMAIL PASSWORD

    def crawl_product(self):
        print("==============================")
        print("method crawl_product")
        self.driver.get('http://prod.danawa.com/list/?cate=112752')
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        main_prodlist = soup.select('div.prod_info > p > a')
        
        for product in main_prodlist:
            n = product.text.lstrip().rstrip()
            url = product.get('href')

            product, created = Product.objects.get_or_create(
                name = n
            )

            if created:
                print("Create |", n)       
            if product.url == '':
                print("URL write", url)
                product.url = url

            product.save()

        now = timezone.now()
        print("Done at", now, ",", len(main_prodlist), "items")

    def crawl_price(self):
        print("==============================")
        print("method crawl_price")
        now = timezone.now()
        for product in Product.objects.all():
            self.driver.get(product.url)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            price = [int(p.text[:-1].replace(',', '')) for p in soup.select('span.lwst_prc')]
            price_min = min(price)

            try:
                latest_price = product.price_set.latest('date')
                latest_date = latest_price.date.date()
                if latest_date == now.date() and latest_price.price == price_min:
                    continue
            except:
                print("Error | latest_price DoesNotExist, Product :", product.name)


            product.price_set.create(
                date = timezone.now(),
                price = price_min
            )
            print("Save |", product.name)
            product.save()

        now = timezone.now()
        print("Done at", now, ",", len(Product.objects.all()), "items")


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
    c.crawl_product()
    c.crawl_price()
    c.mailing()