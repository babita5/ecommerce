from django.db import models
from django.urls import reverse
STATUS=(('In','In Stock'),('Out','Out of Stock'))
LABEL=(('new','New Product'),('hot','Hot Product'),('sale',"Sale product"))
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=300)
    slug=models.CharField(max_length=300, unique=True)
    image=models.ImageField(upload_to='media')
    def __str__(self):
        return self.name
    def get_category_url(self):
        return reverse('online:category',kwargs={'slug':self.slug})

class Slider(models.Model):
    name=models.CharField(max_length=400)
    image=models.ImageField(upload_to='media')
    description=models.TextField()
    url=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    name=models.CharField(max_length=300)
    rank=models.IntegerField(unique=True)
    image=models.ImageField(upload_to='media')
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=300)
    image=models.ImageField(upload_to='media')
    rank=models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    def get_brand_url(self):
        return reverse('online:brand',kwargs={'name':self.name})

class Item(models.Model):
    title=models.CharField(max_length=300)
    price=models.IntegerField()
    slug=models.CharField(max_length=300, unique=True)
    discounted_price=models.IntegerField(default=0)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    status=models.CharField(max_length=50, choices= STATUS)
    label=models.CharField(max_length=60, choices= LABEL, default='new')
    image=models.ImageField(upload_to='media')

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('online:product',kwargs={'slug':self.slug})

    def get_cart_url(self):
        return reverse('online:add-to-cart',kwargs={'slug':self.slug})

class Cart(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    slug=models.CharField(max_length=200)
    quantity=models.IntegerField(default=1)
    user=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now=True)
    total=models.IntegerField()

    def __str__(self):
        return self.user

    def delete_get_cart_url(self):
        return reverse('online:delete-cart',kwargs={'slug':self.slug})

    def delete_single_cart_url(self):
        return reverse('online:delete-single-cart',kwargs={'slug':self.slug})

class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    subject=models.TextField()
    message=models.TextField()

    def __str__(self):
        return self.name
