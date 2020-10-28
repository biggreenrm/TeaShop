from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Orders
import braintree


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Accepting token for transaction creating
        nonce = request.POST.get('payment_method_nonce', None) # formed in template by JS SDK
        # Creating and saving of transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
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