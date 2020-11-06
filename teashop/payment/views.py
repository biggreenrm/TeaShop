from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Orders
import braintree
import weasyprint
from io import BytesIO


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Orders, id=order_id)
    
    if request.method == 'POST':
        # Accepting token for transaction creating
        nonce = request.POST.get('payment_method_nonce', None) # formed in template by JS SDK
        # Creating and saving of transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_sum()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True # it means that transaction will be processed automatically
            }
        })
        if result.is_success:
            # Mark order as paid
            order.paid = True
            # Save transaction ID into order
            order.braintree_id = result.transaction.id
            order.save()
            
            # Creating email message
            subject = f'TeaShop - Invoice no. {order.id}'
            message = 'Please, find atteched invoice for your recent purchase.'
            email = EmailMessage(subject,
                                 message,
                                 'admin@myteashop.com',
                                 [order.email])
            # Creating PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            # Attach PDF to email
            email.attach(f'order_{order.id}.pdf',
                         out.getvalue(),
                         'application/pdf')
            # Sending message
            email.send()
            
            return redirect('payment:done')
        else:
            return redirect('payment: canceled')
    else:
        # Creating disposable token for JavaScript SDK
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')