# Django stuff
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# this decorator simply checks if user 'is_active' and 'is_staff'
from django.contrib.admin.views.decorators import staff_member_required

# Project inner things
from .models import OrderItem, Orders
from .forms import OrdersCreateForm
from .tasks import order_created
from cart.cart import Cart

# Third party
import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrdersCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # create model's object without saving to db
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    coupon = order.coupon
    # it doesn't return response, but html as a string
    html = render_to_string('orders/order/pdf.html',
                            {'order': order,
                             'coupon': coupon})
    
    # set-up response as a downloadable pdf-file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=\
        "order_{order.id}"'
        
    # make pdf from html-string and write it into response
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])

    return response
