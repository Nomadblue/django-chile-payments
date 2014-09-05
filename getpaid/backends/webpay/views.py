# coding: utf-8

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from getpaid.models import Payment
from . import PaymentProcessor, webpay_run


@require_POST
@csrf_exempt
def pago(request, pk):
    with webpay_run('tbk_bp_pago.cgi', pk) as cgi:
        params = request.body + "\n"
        output, _ = cgi.communicate(params)
        _, body = output.split("\n\n")
        return HttpResponse(body)


@require_POST
@csrf_exempt
def resultado(request, pk):
    with webpay_run('tbk_bp_resultado.cgi', pk) as cgi:
        params = request.body + "\n"
        output, _ = cgi.communicate(params)
        _, body, _ = output.split("\n\n")
        return HttpResponse(body)


@require_POST
@csrf_exempt
def close(request):
    answer = request.POST.get('TBK_RESPUESTA', None)

    try:
        payment_pk = int(request.POST['TBK_ID_SESION'])
    except:
        if (answer == u'0'):
            return HttpResponse('RECHAZADO')
        else:
            return HttpResponse('ACEPTADO')

    # Check if 'orden de compra' was already paid in another Payment before
    order_id = int(request.POST['TBK_ORDEN_COMPRA'])
    print "Orden de compra: %s" % order_id
    previous_payments = Payment.objects.filter(order__id=order_id, status='paid', backend='getpaid.backends.webpay')
    if previous_payments:
        return HttpResponse('RECHAZADO')

    try:
        payment = Payment.objects.get(pk=payment_pk,
                                      status='in_progress',
                                      backend='getpaid.backends.webpay')
    except Payment.DoesNotExist:
        if (answer == u'0'):
            return HttpResponse('RECHAZADO')
        else:
            return HttpResponse('ACEPTADO')

    if (answer == u'0'):
        if PaymentProcessor.validate(payment, request):
            payment.on_success()
            return HttpResponse('ACEPTADO')
        else:
            payment.on_failure()
            return HttpResponse('RECHAZADO')
    else:
        payment.on_failure()
        return HttpResponse('ACEPTADO')


@require_POST
@csrf_exempt
def success(request):
    payment_pk = request.POST.get('TBK_ID_SESION')
    try:
        payment = Payment.objects.get(pk=payment_pk, paid_on__isnull=False)
    except (Payment.DoesNotExist, ValueError):
        return redirect('getpaid-webpay-failure')
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


@csrf_exempt
def failure(request):
    context = {'order_id': request.POST.get('TBK_ORDEN_COMPRA')}
    return render(request, 'getpaid/failure.html', context)
