from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path("", market_home, name="market_home"),
    path("become-seller/", become_seller, name="become_seller"),
    path("add-product/", add_product, name="add_product"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("cart/", cart_view, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),  # ✅ Added this!
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", remove_cart_item, name="remove_cart_item"),
]