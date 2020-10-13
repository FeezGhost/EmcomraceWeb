from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True , blank= True)
    email = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank= True)
    price = models.FloatField()
    digital= models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='placeholder.png')
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer =  models.ForeignKey(Customer,  on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank= True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product =  models.ForeignKey(Product,  on_delete=models.SET_NULL, blank=True, null=True)
    order =  models.ForeignKey(Order,  on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0 ,  null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class Shipping(models.Model):
    Customer =  models.ForeignKey(Customer,  on_delete=models.SET_NULL, blank=True, null=True)
    order =  models.ForeignKey(Order,  on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank= True)
    city = models.CharField(max_length=200, null=True, blank= True)
    state = models.CharField(max_length=200, null=True, blank= True)
    zip_code = models.CharField(max_length=200, null=True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

    

    