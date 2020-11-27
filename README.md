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
### Features for customers

This is a **main page** of TeaShop. It provides opportunities to change sorts of tea (groups), open selected tea details and also the link to the customer's cart.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/main_screen.png)


After clicking on any tea image or title user will be redirected to **detail page**, where product may be added to the cart in any amount.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/product_details.png)


Items in cart are saved to **the session**, so user don't have to worry about loosing something from his cart and there is no need to do something twice.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/cart_panel.png)


By clicking on cart panel customer will be redirected to the **cart detail page**. It has all neccesary information about products, its cost, amounts and total amount.
Also there is a special **coupon system integrated** in this web-shop (some kind of discount system). Coupons has its duration and date of expiry.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/cart_details.png)


After clicking on checkout button customer will land to the page with **checkout** form where he will be asked to fill the information about him to deal with **payment and delivery**.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/Checkout.png)


In this project I use **BrainTree payment system** (Uber's partner). It is customizable, easy to setting up, but my favourite opportunity is their sandbox. It means that me as a developer don't need to connect my bank account or get through difficult procces of binding application with it to simply try this system out and test it.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/payment_braintree.png)

Result looks like this:

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/result.png)


In this moment I finished with **cutomer's side features** and want to represent the **administration features** (business side features).


### Features for business (administration)

After end of payment, it is necessary to **sent email to customer** with all information about order and its status. This project use best practice for it - **Celery as a distributed task queue**. It gives an ability to send email in background and eliminates need for user to wait for the end of this operation. In case of any trouble, if there is an error while sending message, Celery will try to resend it until it works. Celery also can be used for any tasks (especially in area of business logic), running which in backround can reduce time of users waiting and doing nothing. 
TeaShop uses **RabbitMQ** as a broker between application and Celery.
Example of sended message (shown in terminal, but easily can be configured to work with **SMTP**).

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/celery_worker.png)


All businesses need a paper document flow, so TeaShop web-application automatically generates **invoice in pdf-format**, that can be printed or used in any way. 

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/invoice.png)


Document flow also needs a common view of all orders (or selected queue). In this case I add feature that write down selected orders in **csv file**.

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/export_csv.png)

Result looks like this:

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/csv.png)


## Summary
TeaShop is a good example of how to use Django to build stable and scalable basic shop with wide functionality for all needs of small and medium business. It uses popular techologies, so you don't need to worry about updates and support in case you decide to integrate some new features. 

## Project status
Work on new features
