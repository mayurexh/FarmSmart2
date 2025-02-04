from django.urls import path
from . import views

urlpatterns = [
    path('first/', views.first, name= "first"),
    path('', views.home, name='home'),
    path('crop-predict/', views.crop_prediction, name='crop_prediction'),
    path('fertilizer-predict/', views.fert_recommend, name='fert_recommend'),
    path('disease-predict/', views.disease_prediction, name='disease_prediction'),
]
