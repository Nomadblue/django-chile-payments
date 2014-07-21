from decimal import Decimal
from django.shortcuts import get_object_or_404
from getpaid.models import Payment
from paypal.pro.views import PayPalPro


def authorization(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    TWOPLACES = Decimal(10) ** -2

    amount = str(payment.amount.quantize(TWOPLACES))

    item = {'amt': amount,
            'invnum': payment.pk,
            'cancelurl': payment.order.get_absolute_url(),
            'returnurl': payment.order.get_absolute_url()}

    kw = {'item': item,
          'payment_template': 'getpaid/paypal_payment.html',
          'confirm_template': 'getpaid/paypal_confirm.html',
          'success_url': payment.order.get_absolute_url(),  # FIX
          'fail_url': payment.order.get_absolute_url()}  # FIX
    ppp = PayPalPro(**kw)
    return ppp(request)
