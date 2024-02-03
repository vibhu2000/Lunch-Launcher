from django import forms
from .models import Cart, Menu, Order

class CartForm(forms.ModelForm):
    class Meta:
        model=Cart
        fields=["quantity"]

class MenuForm(forms.ModelForm):
    class Meta:
        model=Menu
        fields=["name","desc","image","price"]

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=["track"]