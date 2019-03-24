from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField('date')
    price = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.date) + " : " +str(self.price)

class Subscriber(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    registration_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    email = models.EmailField(max_length=254)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=987654321)

    def email_hidden(self):
        email = self.email
        name, domain = email.split('@')
        name = name[:len(name)//2] + '*' * (len(name) - len(name)//2)
        return name + '@' + domain

    def __str__(self):
        return str(self.email)