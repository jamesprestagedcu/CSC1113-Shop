from django.urls import path
from . import views
from .forms import *

urlpatterns = [
   path('', views.index, name="index"),
   path('products/', views.all_products, name='all_products'),
   path('products/<int:prodid>/', views.product_individual, name='individual_product'),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('login/', views.UserLoginView.as_view(), name="login"),
   path('logout/', views.logout_user, name="logout"),
]