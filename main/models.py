from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField('date')
    price = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.date.date()) + " : " +str(self.price)