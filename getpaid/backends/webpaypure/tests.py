import urllib
from collections import OrderedDict
from itertools import starmap
from mock import Mock
from model_mommy import mommy
from django.test import TestCase
from django.utils.timezone import now
from getpaid.backends.webpaypure import PaymentProcessor
import getpaid


class PaymentProcessorTestCase(TestCase):
    REQUEST_PARAMS = OrderedDict((('TBK_ORDEN_COMPRA', '634185'),
                                  ('TBK_TIPO_TRANSACCION', 'TR_NORMAL'),
                                  ('TBK_RESPUESTA', '0'),
                                  ('TBK_MONTO', '11900000'),
                                  ('TBK_CODIGO_AUTORIZACION', '908315'),
                                  ('TBK_FINAL_NUMERO_TARJETA', '6623'),
                                  ('TBK_FECHA_CONTABLE', '0611'),
                                  ('TBK_FECHA_TRANSACCION', '0611'),
                                  ('TBK_HORA_TRANSACCION', '120920'),
                                  ('TBK_ID_SESION', '90'),
                                  ('TBK_ID_TRANSACCION', '250296335'),
                                  ('TBK_TIPO_PAGO', 'VN'),
                                  ('TBK_NUMERO_CUOTAS', '0'),
                                  ('TBK_VCI', 'TSY'),
                                  ('TBK_MAC', '5a778312498c624289a3b4660b8a914ee0da3770bedbbcc564b7908bb85e336fb1ee84d4c7d03ce2a0bdf12300eddb7dd06d1279ff20422e32c6736c5c6fdbe57559e89baa308f893b31d0094cb9dfc50d9f238f2db4432c4c398bd0d5fdf138c104314b1d3331223cae755732856edb307e0815868edbdd98e55dc8f2d8e5bdc7813d11353abb31f1993d6cf82a87d5ac0017974204d6090116e5c273a26392e42e6defb451c0289dd1003b743403f409a31670e6c0031a1e064ec81312b787a35046117124f28e5feb131f00c0f8f3d2f8d333237565f62f5e5767c5418d6b968b9d1b1b15abe7f6010d658ae7051a8d64737192eb43af58e7bcb2bbbea7b6a3cb4e8fcf0d0bb0576822e1bf0db744ad86ce7818961bbea81e184322a3a429abd96a6749884b7737e410fd0af4723b5628ccbd37a91ef3e37a58dff52f304aeda5ba60ac40943753871550dec8b1b09bde70f49df11059cfe757b65abd19e8e838b110ff1b0ddd6200d653db587a2ba58749cbc5f1d9108b4136b628f93401f83ead1cc835c1ec9a841cf290667e205a9b46c250d1f1932ec917499e61839422097473b0ee7b163f2b10413dd1f4f1b73713cf01797bdac20aacf9b28850127a9e24e3cbd361b460c9133d64a7c59afc41cdba92d01178e9')))

    REQUEST_BODY = "&".join(starmap("{}={}".format, REQUEST_PARAMS.items()))
    QUOTED_REQUEST_BODY = urllib.quote(REQUEST_BODY)

    def test_payment_ok(self):
        payment = mommy.make(getpaid.models.Payment, id=90, amount=119000, paid_on=None)

        request = Mock()
        request.POST = {'TBK_MONTO': '11900000'}
        request.body = self.QUOTED_REQUEST_BODY

        self.assertTrue(PaymentProcessor.validate(payment, request))

    def test_payment_diff_amount(self):
        payment = mommy.make(getpaid.models.Payment, id=90, amount=1190000, paid_on=None)

        request = Mock()
        request.POST = {'TBK_MONTO': '11900000'}
        request.body = self.QUOTED_REQUEST_BODY

        self.assertFalse(PaymentProcessor.validate(payment, request))

    def test_payment_mac_invalid(self):
        payment = mommy.make(getpaid.models.Payment, id=90, amount=119000, paid_on=None)

        request = Mock()
        request.POST = {'TBK_MONTO': '11900000'}
        request.body = self.QUOTED_REQUEST_BODY[:-1]

        self.assertFalse(PaymentProcessor.validate(payment, request))

    def test_payment_already_paid(self):
        payment = mommy.make(getpaid.models.Payment, id=90, amount=119000, paid_on=now())

        request = Mock()
        request.POST = {'TBK_MONTO': '11900000'}
        request.body = self.QUOTED_REQUEST_BODY

        self.assertFalse(PaymentProcessor.validate(payment, request))
