from django import forms
from .models import Seller, Product

class SellerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['phone', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
