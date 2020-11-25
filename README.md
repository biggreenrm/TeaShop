# TeaShop

TeaShop is a web-application for selling good chinese tea that is build mainly with Django Framework. But it is not bound only for tea subject and after some changes can
be used for selling everything, because of all needed base functions and opportunities. The main features of this web-shop: user sessions, customer's carts,
braintree pay service, availability of Celery for background tasks and many others. All features will be described below.

## Installation

Simply clone the repo and install requirements
```
pip install -r requirements.txt
```
Also don't forget to install RabbitMQ as a message broker.

## Usage

To start work you have to start RabbitMQ server, Celery worker and after that - django-server.

```
rabbitmq-server
celery -A teashop worker -l info
python manage.py runserver
```
If you run app first time - firstly make migrations.

## Features

This is a main page of TeaShop. It provides opportunities to change sorts of tea (groups), open selected tea details and also the link to the customer's cart.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/main_screen.png)

After clicking on any tea image or title user will be redirected to detail page, where product may be added to the cart in any amount.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/product_details.png)

Items in cart are saved to the session, so user don't have to worry about loosing something from his cart and there is no need to do something twice.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/cart_panel.png)

By clicking on cart panel customer will be redirected to the cart detail page. It has all neccesary information about products, its cost, amounts and total amount.
Also there is a special coupon system integrated in this web-shop (some kind of discount system). Coupons has its duration and date of expiry.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/cart_details.png)

After clicking on checkout button customer will land to the page with checkout form where he will be asked to fill the information about him to deal with payment and delivery.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/Checkout.png)

In this project I use BrainTree payment system (Uber's partner). It is customizable, easy to setting up, but my favourite opportunity is their sandbox. It means that me as a developer don't need to connect my bank account or get through difficult procces of binding application with it to simply try this system out and test it.
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/payment_braintree.png)
![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/result.png)

In this moment I finished with cutomer's side features and want to represent the administration features (business side features). 
