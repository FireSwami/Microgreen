from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from green.models import Green
from cart.models import Order, OrderLineItem

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Green, id=product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=True)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Green, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    if request.method == "POST":
        order = Order(user=request.user, final_price=cart.get_total_price())
        order.save()
        for row in cart:
            line_item = OrderLineItem(
                order=order,
                product=row["product"],
                quantity=row["quantity"],
                price=row["price"],
            )
            line_item.save()
        cart.clear()
        success_url = reverse_lazy('cart:buythanks')
        return redirect(success_url)
    else:
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                       'update': True})
        return render(request, 'cart/detail.html', {'cart': cart})


def buythanks(request):
    return render(request, 'cart/buythanks.html')
