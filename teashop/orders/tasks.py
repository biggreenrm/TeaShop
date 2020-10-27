# Here Celery would find async tasks for project
from celery import task
from django.core.mail import send_mail
from .models import Orders


@task
def order_created(order_id):
    # function sends e-mail to customer in case of successful order
    # it takes all needed info from object of Orders model
    order = Orders.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\nYou have successfully placed order.\
                Your order id is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])