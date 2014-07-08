# coding: utf-8

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from getpaid.models import Payment
from . import PaymentProcessor


@require_POST
@csrf_exempt
def notify(request):
    return HttpResponse(PaymentProcessor.validate(request))


@require_POST
@csrf_exempt
def success(request):
    payment_pk = request.POST['TBK_ID_SESION']
    payment = Payment.objects.get(pk=payment_pk)
    order = payment.order
    params = payment.journalentry.params

    PAYMENT_TYPE_DESCRIPTIONS = {u'VN': u'Crédito',
                                 u'VC': u'Crédito',
                                 u'SI': u'Crédito',
                                 u'CI': u'Crédito',
                                 u'VD': u'Redcompra'}

    INSTALLMENT_TYPE_DESCRIPTIONS = {u'VN': u'Sin cuotas',
                                     u'VC': u'Cuotas normales',
                                     u'SI': u'Sin interés',
                                     u'CI': u'Cuotas comercio',
                                     u'VD': u'Venta débito'}

    context = {'payment_items': order.items,
               'order': payment.order,
               'site_url': settings.SITE_URL,
               'customer_name': order.customer_name,
               'order_id': order.pk,
               'payment_type': PAYMENT_TYPE_DESCRIPTIONS[params['TBK_TIPO_PAGO']],
               'installment_type': INSTALLMENT_TYPE_DESCRIPTIONS[params['TBK_TIPO_PAGO']],
               'last_digits': params['TBK_FINAL_NUMERO_TARJETA'],
               'transaction_date': payment.paid_on,
               'authorization_code': params['TBK_CODIGO_AUTORIZACION'],
               'amount': "{} ${}".format(payment.currency, int(payment.amount)),
               'installments': params['TBK_NUMERO_CUOTAS'].zfill(2)}
    return render(request, 'getpaid/success.html', context)


@require_POST
@csrf_exempt
def failure(request):
    context = {'order_id': request.POST['TBK_ORDEN_COMPRA']}
    return render(request, 'getpaid/failure.html', context)
