from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# this decorator simply checks if user 'is_active' and 'is_staff'
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Orders
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

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})