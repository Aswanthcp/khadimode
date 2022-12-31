from django.db import models

from accounts.models import Account
from store.models import Product, Variation


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=150)
    address_line_1 = models.TextField(null=False)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150,null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name }{self.last_name}"

    def full_address(self):
        return f"{self.address_line_1 } { self.address_line_2}"

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)


class OrderItems(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)
    status          =   models.CharField(max_length=50,choices=STATUS,default='New')


    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)


class ProfileAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address_line_1 = models.TextField(null=False)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    defualt = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

class Coupons(models.Model):
    coupon_name = models.CharField(max_length=250)
    coupon_code = models.CharField(max_length=50)
    coupon_offer = models.IntegerField()
    coupon_min = models.IntegerField()
    coupon_start = models.DateTimeField(default=None)
    coupon_end = models.DateTimeField(default=None)