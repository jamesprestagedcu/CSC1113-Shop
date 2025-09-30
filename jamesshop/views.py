from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import * 
from decimal import Decimal

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
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        if sbi.exists():
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'basket.html', {'empty':True})


@login_required
def add_to_basket(request, prodid):
    user = request.user
    product = get_object_or_404(Product, id=prodid)

    basket, created = Basket.objects.get_or_create(user_id=user, is_active=True)

    sbi = BasketItem.objects.filter(basket_id=basket, product_id=product).first()

    if sbi is None:
        sbi = BasketItem.objects.create(basket_id=basket, product_id=product, quantity=1)
    else:
        sbi.quantity += 1
        sbi.save()

    return redirect('all_products')

@login_required
def remove_item(request,sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity-1
            basketitem.save() 
        else:
            basketitem.delete() 
    return redirect("/basket")

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

@login_required
def order(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists(): 
        return redirect("/")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = Decimal("0.00")
            for item in sbi:
                total += item.item_price()
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order': order, 'basket': basket, 'sbi': sbi})
        else:
            return render(request, 'orderform.html', {'form': form, 'basket': basket, 'sbi': sbi})
    else:
        form = OrderForm()
        return render(request, 'orderform.html', {'form': form, 'basket': basket, 'sbi': sbi})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})