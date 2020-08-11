from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_image = models.ImageField(upload_to="images/", default='images/default.png')

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, choices=CATEGORY)
    description = models.TextField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delieverd', 'Delieverd')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)
    note = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Name: {self.customer} Bought Product: {self.product}"
