from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class SetProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.EmailField(blank=True, null=True)
    fname=models.CharField(max_length=25, blank=True)
    lname=models.CharField(max_length=25, blank=True)
    address=models.TextField(null=True)
    phone=models.CharField(max_length=10, blank=True)
    image=models.ImageField(upload_to='image/', null=True, blank=True, default="static/images/log.png")
    def __str__(self):
        return self.user.username

# tuple
Category_Choice=(
    # batabase   form
    ('Pasta', 'Pasta'),
    ('Pizza', 'Pizza'),
    ('Burger', 'Burger'),
    ('Sandwich', 'Sandwich'),
    ('Snacks', 'Snacks'),
    ('Beverages', 'Beverages')
)
Types_Choice=(
    ('Vegetarian', 'Vegetarian'),
    ('Non-Vegetarian', 'Non-Vegetarian')
)
class Menu(models.Model):
    name=models.CharField(max_length=100, blank=True)
    desc=models.TextField(null=True)
    cate=models.CharField(choices=Category_Choice, default='Snacks', max_length=100)
    image=models.ImageField(upload_to='food/', null=True, blank=True)
    price=models.FloatField(blank=True, null=True)
    types=models.CharField(choices= Types_Choice, default='Vegetarian', max_length=100)
    def __str__(self):
        return self.name

    @staticmethod
    def get_menu_by_cate(cate):
        if cate:
            #                           form = upper define variable
            return Menu.objects.filter(cate=cate)
        else:
            return Menu.objects.all()

    @staticmethod
    def get_menu_by_type(types):
        if types:
            return Menu.objects.filter(types=types)
        else:
            return Menu.objects.all()

class Cart(models.Model):
    user =models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Menu,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def total_price(self):
        return self.quantity*self.product.price

class Contact(models.Model):
    name=models.CharField(max_length=25, blank=True)
    email=models.EmailField(blank=True, null=True)
    message=models.TextField(null=True)
    def __str__(self):
        return self.name

Track_Choice=(
    ('Pending Seller Approval','Pending Seller Approval'),
    ('Your Order is Accepted','Your Order is Accepted'),
    ('Your Order start Cooking','Your Order start Cooking'),
    ('Your Order has been Dispatch','Your Order has been Dispatch'),
    ('Your Order has been Delivered','Your Order has been Delivered')
)

class Order(models.Model):
    user=models.ForeignKey(User,on_delete = models.CASCADE)
    menu=models.CharField(max_length=200)
    total_price=models.FloatField(blank=True, null=True)
    status = models.BooleanField(default=False)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    track = models.CharField(choices= Track_Choice, default='Pending Seller Approval', max_length=100)
    def __str__(self):
        return self.user.username

# list
RATE_CHOICES = [
    ('BAD','BAD'),
    ('AVERAGE','AVERAGE'),
    ('GOOD','GOOD'),
    ('AWESOME','AWESOME'),
    ('DELICIOUS','DELICIOUS')
]


class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete = models.CASCADE)
    order=models.ForeignKey(Menu,on_delete = models.CASCADE)
    review = models.CharField(max_length=300, null=True)
    rate = models.CharField(choices=RATE_CHOICES, max_length=10)
    def __str__(self):
        return self.user.username