from django.shortcuts import get_object_or_404
from getpaid.models import Payment
from paypal.pro.views import PayPalPro


def authorization(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    item = {'amt': payment.amount,
            'invnum': payment.pk,}

    kw = {'item': item,
          'payment_template': 'getpaid/paypal_payment.html',
          'confirm_template': 'getpaid/paypal_confirm.html',
          'success_url': '/success/',  # FIX
          'fail_url': '/fail/'}  #FIX
    ppp = PayPalPro(**kw)
    return ppp(request)
