from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrdersCreateForm
from .tasks import order_created
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
            # running async task
            order_created.delay(order.id)
            # save order in session
            request.session['order_id'] = order.id
            # redirect to the payment page
            return redirect(reverse('payment:process'))
    else:
        form = OrdersCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
        