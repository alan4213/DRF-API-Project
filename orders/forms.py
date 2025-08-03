from django.forms import ModelForm

from .models import Order

class AddressForm(ModelForm):

    class Meta:

        model=Order

    # fields=['title', 'rating']#for getting specific fields

        fields=['shipping_name',

        'shipping_phone',

        'shipping_email',

        'shipping_address',

        'shipping_city',

        'shipping_state',

        'shipping_pincode',

        'shipping_country']