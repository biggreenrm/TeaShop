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

![Alt text](https://github.com/biggreenrm/TeaShop/blob/master/readme_screenshots/main_screen.png)
