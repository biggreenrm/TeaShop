from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedMultipleChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                              coerce=int) #automatically convert value into int (doesn't work)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)