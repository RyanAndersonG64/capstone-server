import datetime
from django.db import models

# Create your models here.

class Vehicle(models.Model):
    type = models.TextField(max_length=100)
    number_in_stock = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.type} - {self.number_in_stock} in stock'

class Customer(models.Model):
    name = models.TextField(max_length=100)
    bicycles_owned = models.SmallIntegerField(default=0)
    unicycles_owned = models.SmallIntegerField(default=0)
    tricycles_owned = models.SmallIntegerField(default=0)
    mountain_bikes_owned = models.SmallIntegerField(default=0)
    bmx_bikes_owned = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_date = models.DateField(default=datetime.datetime.now())
    number = models.SmallIntegerField(default = 1)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order ID {self.id} : {self.customer} ordered {self.number} {self.order.type}s on {self.created_date}.  Their payment status is {self.paid}.'