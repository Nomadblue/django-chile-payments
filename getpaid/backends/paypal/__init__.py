from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from getpaid.backends import PaymentProcessorBase
from paypal.pro import signals as wpp_signals


class PaymentProcessor(PaymentProcessorBase):
    BACKEND = 'getpaid.backends.paypal'
    BACKEND_NAME = _('Paypal backend')
    BACKEND_ACCEPTED_CURRENCY = ('USD',)

    def get_gateway_url(self, request):
        return reverse('getpaid-paypal-authorization', kwargs={'pk': self.payment.pk}), "GET", {}


def payment_successful(sender, *args, **kwargs):
    from getpaid.models import Payment
    payment = Payment.objects.get(pk=kwargs['invnum'])
    payment.on_success()


def payment_flagged(sender, *args, **kwargs):
    from getpaid.models import Payment
    payment = Payment.objects.get(pk=kwargs['invnum'])
    payment.on_failure()


wpp_signals.payment_was_successful.connect(payment_successful)
wpp_signals.payment_was_flagged.connect(payment_flagged)
