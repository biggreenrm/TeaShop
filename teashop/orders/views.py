from django.shortcuts import render
from .models import OrderItem
from .forms import OrdersCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrdersCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            # bind every item in cart to customers order
            # information is get from cart also
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # after making an order there is no need to keep cart
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrdersCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
        