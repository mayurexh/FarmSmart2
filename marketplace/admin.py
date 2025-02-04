from django.contrib import admin
from .models import Order, Seller, Product, CartItem
# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    
admin.site.register(Seller,SellerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'get_username')
    
    #lookup for foreign keeys
    def get_username(self, obj):
        return obj.seller.user.username
    get_username.short_description = "User" #Renames column head
    
admin.site.register(Product, ProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('get_user','get_product', 'quantity')
    
    def get_user(self,obj):
        return obj.user.username
    get_user.short_description = "User"
    
    def get_product(self, obj):
        return obj.product.name
    get_product.short_description = "Product"
    
admin.site.register(CartItem, CartAdmin)