from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """
    Class for shopping cart.
    """
    
    def __init__(self, request):
        """
        Initialization of cart object.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # save empty cart into session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart # cart's content (it is dictionary), not cart itself

    def __iter__(self):
        """
        Iterating through products in cart and and accepting relevant Product's objects.
        """
        product_ids = self.cart.keys()
        # retrieving objects and transfer them to cart
        products = Product.objects.filter(id__in=product_ids)
        # this new cart almost the same as self.cart, but have one
        # additional key - 'product', with value as model's object
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # price should become decimal, because strings cannot be avaluated
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item    
    
    def __len__(self):
        """
        Returns summary of products in cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Returns total price for all products in cart.
        """
        return sum(
            item['quantity'] * Decimal(item['price'])
            for item in self.cart.values()
        )    
    
    def save(self):
        """
        Mark session as modified, so django save it.
        """
        # somehow Django understands, that modified sessions should be saved
        self.session.modified = True
    
    # how to decide where to place functionality?
    # it is OOP, so place it where it could be placed in real world    
    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product to cart and refresh its quantity.
        """
        # in JSON only strings can be keys
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            
        # if true - replace previous quantity on a new one (choosed by customer)
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            
        # if not true - add (usually +1) to previous quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def remove(self, product):
        """
        Removing product from cart.
        """"
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def clear(self):
        """
        Removing all products from cart.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()