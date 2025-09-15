from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('products/', views.all_products, name='all_products'),
   path('products/<int:prodid>/', views.product_individual, name='individual_product')
]