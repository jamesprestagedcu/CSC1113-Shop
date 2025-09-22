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