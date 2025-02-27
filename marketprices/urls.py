from django.urls import path, include
from .import views
urlpatterns = [
   path("", views.market_prices_page, name= "market_prices"),
   path("search-prices/", views.search_prices, name="search_prices")
]