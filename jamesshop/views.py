from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import * 

def index(request):
    return render(request, 'index.html')

@login_required
def all_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def product_individual(request, prodid):
    product = get_object_or_404(Product, id=prodid)
    return render(request, 'individual_product.html', {'product': product})

@login_required
def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user 
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the product 
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # create one 
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name='login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

def logout_user(request):
    logout(request)
    return redirect("/")