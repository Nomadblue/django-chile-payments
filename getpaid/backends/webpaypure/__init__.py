import rsa
import random
import base64
import hashlib
import datetime
import requests
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from collections import OrderedDict
from operator import methodcaller
from itertools import starmap
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from getpaid.backends import PaymentProcessorBase
from getpaid import models as getpaid_models
from models import JournalEntry

TBK_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtKe3HHWwRcizAfkbS92V
fQr8cUb94TRjQPzNTqBduvvj65AD5J98Cn1htE3NzOz+PjPRcnfVe53V4f3+YlIb
6nnxyeuYLByiwoPkCmpOFBxNp04/Yh3dxN4xgOANXA37rNbDeO4WIEMG6zbdQMNJ
7RqQUlJSmui8gt3YxtqWBhBVW79qDCYVzxFrv3SH7pRuYEr+cxDvzRylxnJgr6ee
N7gmjoSMqF16f9aGdQ12obzV0A35BqpN6pRFoS/NvICbEeedS9g5gyUHf54a+juB
OV2HH5VJsCCgcb7I7Sio/xXTyP+QjIGJfpukkE8F+ohwRiChZ9jMXofPtuZYZiFQ
/gX08s5Qdpaph65UINP7crYbzpVJdrT2J0etyMcZbEanEkoX8YakLEBpPhyyR7mC
73fWd9sTuBEkG6kzCuG2JAyo6V8eyISnlKDEVd+/6G/Zpb5cUdBCERTYz5gvNoZN
zkuq4isiXh5MOLGs91H8ermuhdQe/lqvXf8Op/EYrAuxcdrZK0orI4LbPdUrC0Jc
Fl02qgXRrSpXo72anOlFc9P0blD4CMevW2+1wvIPA0DaJPsTnwBWOUqcfa7GAFH5
KGs3zCiZ5YTLDlnaps8koSssTVRi7LVT8HhiC5mjBklxmZjBv6ckgQeFWgp18kuU
ve5Elj5HSV7x2PCz8RKB4XcCAwEAAQ==
-----END PUBLIC KEY-----
"""

PRIVADA_PEM = """
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAn3HzPC1ZBzCO3edUCf/XJiwj3bzJpjjTi/zBO9O+DDzZCaMp
14aspxQryvJhv8644E19Q+NHfxtz1cxd2wnSYKvay1gJx30ZlTOAkzUj4QMimR16
vomLlQ3T2MAz1znt/PVPVU7T/JOG9R+EbiHNVKa/hUjwJEFVXLQNME97nHoLjb3v
V5yV2aVhmox7b54n6F3UVPHvCsHKbJpXpE+vnLpVmdETbNpFVrDygXyG+mnEvyiO
BLIwEY3XTMrgXvS069groLi5Gg8C5LDaYOWjE9084T4fiWGrHhn2781R1rykunTu
77wiWPuQHMS0+YC7mhnsk8Z/ilD+aWz/vhsgHwIDAQABAoIBAQCM+Nrt4cpNKQmn
+Ne8348CGRS9ACXp6WRg6OCQXO4zM7lRZAminVgZgSQXE6aJR+T9rIWMeG7GWydX
aJGzEEQJZOjV0MkUr+7mk9qiTOGkGHmGlyHnRQU8jDU59vXe3UEl3l5+NmwHbQht
waf9F7XLmoLK/WoVJA6tICRpCl1oQrpziqN+gjdmMpz9i8I1sMFE7+Y7xf+7S2u7
c1MRPUWqgdS9yViQVh3vZi25m5CyKRVnOB0hpNuZ7nrJymtADYSWt9wV2W1fX+MX
UUoYfxyQQvWryHhGdedU7GGAnoEdblUcDkBuAaFmsm1P8K4HQZLWP4v6pYlW2JLa
Zoaerb3BAoGBANCRevl0CLB0HBU7sCs0eN9fTkIEsh3OVIxPSBqDnKsynJrIWovK
cs37Vb6phzdQO3ADoFJvR9ck8+v6Cv0KR8IOFl9wfC4ZoxkKBBeq94ZLN+YhE2PW
KiRFybqcgCtzxKS3MyWgpIcT9xFtHVjlorZ8Jk51fgLZbGzamtLhderVAoGBAMO0
mIiiV4l2vXzu4tFfkpu/GOx/D9/vAic3X9FOky09BNCyuMXMQgI8e3wWsGEZghls
Vg9KDV5EPxAmpumcdPFK2IMACaH41ac7vys3ZD8kMK0INQkuDAcG4YsxMaTwEPo0
p1i3zwwEWwknw1yJkOyozz0EcIzS9NrZZEjnBHEjAoGAQ81XdeqzvHEyg/CQd6sq
NCtubGXMZYYi1C4d2Yi5kKn2YRcK4HDi23V+TWodK+0oNWToZIQKjbVUmn0Bv3rt
EvezbDlMFUx+SfCIng0VRJIFTQmpnQYNUxdg2gpwXC/ZWFa6CNxtQABMjFy1cqXM
PJild1IYseJurgBu3mkvBTUCgYBqA/T1X2woLUis2wPIBAv5juXDh3lkB6eU8uxX
CEe2I+3t2EM781B2wajrKadWkmjluMhN9AGV5UZ8S1P0DStUYwUywdx1/8RNmZIP
qSwHAGXV9jI0zNr7G4Em0/leriWkRM26w6fHjLx8EyxDfsohSbkqBrOptcWqoEUx
MOQ5HQKBgAS4sbddOas2MapuhKU2surEb3Kz3RCIpta4bXgTQMt9wawcZSSpvnfT
zs5sehYvBFszL3MV98Uc50HXMf7gykRCmPRmB9S+f+kiVRvQDHfc9nRNg2XgcotU
KAE16PQM8GihQ0C+EcXHouyud5CRJGfyurokRlH/jY3BiRAG5c+6
-----END RSA PRIVATE KEY-----
"""


def aes_cbc_encrypt(message, key=None, key_size=256):
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)
 
    padded_message = pad(message)
 
    if key is None:
        key = Random.OSRNG.posix.new().read(key_size // 8)
 
    iv = Random.OSRNG.posix.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return (iv, key, cipher.encrypt(padded_message))

def aes_cbc_decrypt(ciphertext, key):
    unpad = lambda s: s[:-ord(s[-1])]
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))[AES.block_size:]

    return plaintext


class PaymentProcessor(PaymentProcessorBase):
    BACKEND = 'getpaid.backends.webpaypure'
    BACKEND_NAME = _('Webpay backend in pure Python')
    BACKEND_ACCEPTED_CURRENCY = ('CLP', 'USD')
    TESTING_COMMERCE_IDS = {'CLP': '597026007976',
                            'USD': '597026007984'}
    TBK_PUBLIC_KEY = TBK_PUBLIC_KEY
    PRIVADA_PEM = PRIVADA_PEM

    def get_params(self):
        payment = self.payment
        order = payment.order
        currency = payment.currency
        base_url = settings.SITE_URL
        certified = self.get_backend_setting('CERTIFIED', False)

        if certified:
            commerce_code = self.get_backend_setting('COMMERCE_ID_{}'.format(currency))
        else:
            commerce_code = self.TESTING_COMMERCE_IDS[currency]

        return OrderedDict((('TBK_ORDEN_COMPRA', order.id),
                            ('TBK_CODIGO_COMERCIO', commerce_code),
                            ('TBK_ID_TRANSACCION', int(random.random() * 10000000000)),
                            ('TBK_URL_CGI_COMERCIO', reverse('getpaid-webpaypure-notify')),
                            ('TBK_SERVIDOR_COMERCIO', self.get_backend_setting('STATIC_INBOUND_IP')),
                            ('TBK_PUERTO_COMERCIO', '80'),
                            ('TBK_VERSION_KCC', '6.0'),
                            ('TBK_KEY_ID', '101'),
                            ('PARAMVERIFCOM', '1'),
                            ('TBK_MAC', None),
                            ('TBK_MONTO', str(order.total) + '00'),
                            ('TBK_ID_SESION', payment.id),
                            ('TBK_URL_EXITO', base_url + reverse('getpaid-webpaypure-success')),
                            ('TBK_URL_FRACASO', base_url + reverse('getpaid-webpaypure-failure')),
                            ('TBK_TIPO_TRANSACCION', 'TR_NORMAL')))

    @classmethod
    def get_keys_raw(cls):
        if cls.get_backend_setting('CERTIFIED', False):
            # TODO: End this new line spree
            tbk_public_key = "\n" + cls.get_backend_setting('TRANSBANK_PUBLIC_KEY') + "\n"
            commerce_private_key = "\n" + cls.get_backend_setting('COMMERCE_PRIVATE_KEY') + "\n"
            return (tbk_public_key, commerce_private_key)
        else:
            return (cls.TBK_PUBLIC_KEY, cls.PRIVADA_PEM)

    @classmethod
    def encrypt(cls, message):
        public_key_data, private_key_data = cls.get_keys_raw()

        private_rsa_key = rsa.PrivateKey.load_pkcs1(private_key_data)
        signature = rsa.sign(message, private_rsa_key, 'SHA-512')
        iv, aes_key, encrypted_message = aes_cbc_encrypt(signature + message)
        
        public_key = RSA.importKey(public_key_data.strip())
        public_cipher = PKCS1_OAEP.new(public_key)
        encrypted_key = public_cipher.encrypt(aes_key)

        return base64.b64encode(iv + encrypted_key + encrypted_message)

    @classmethod
    def decrypt(cls, encrypted_message):
        public_key_data, private_key_data = cls.get_keys_raw()

        private_key = RSA.importKey(private_key_data.strip())
        cipher = PKCS1_OAEP.new(private_key)

        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_data)

        data = base64.b64decode(encrypted_message.strip())
        iv = data[0:16]

        encrypted_key = data[16:272]

        key = cipher.decrypt(encrypted_key)

        signed_message = aes_cbc_decrypt(iv + data[272:], key)
        signature, message = signed_message[0:512], signed_message[512:]

        if rsa.verify(message, signature, public_key):
            return message

    def get_token(self):
        params = self.get_params()

        params['TBK_MAC'] = hashlib.md5("&".join(starmap("{}={}".format, filter(lambda param: param[0] != 'TBK_MAC', params.items()))) + params['TBK_CODIGO_COMERCIO'] + 'webpay').hexdigest()  # :facepalm:

        if self.get_backend_setting('CERTIFIED', False):
            token_endpoint_url = 'https://webpay.transbank.cl:443/cgi-bin/bp_validacion.cgi'
        else:
            token_endpoint_url = 'https://certificacion.webpay.cl:6443/webpayserver/bp_validacion.cgi'

        data = {'TBK_VERSION_KCC': '6.0',
                'TBK_CODIGO_COMERCIO': params['TBK_CODIGO_COMERCIO'],
                'TBK_KEY_ID': '101',
                'TBK_PARAM': self.encrypt("#".join(starmap("{}={}".format, params.items())))}

        response = requests.post(token_endpoint_url, data=data)

        r = dict(map(methodcaller('split', '='), self.decrypt(response.content.strip()).strip().split('\n')))

        if r['ERROR'] == '0':
            return r['TOKEN']


    @classmethod
    def validate(cls, request):
        commerce_code = request.POST['TBK_CODIGO_COMERCIO']  # check if ok, if not, return ERR
        decrypted_message = cls.decrypt(request.POST['TBK_PARAM'])
        params = dict(map(methodcaller('split', '='), decrypted_message.split('#')))

        answer = params['TBK_RESPUESTA']

        try:
            payment_pk = int(params['TBK_ID_SESION'])
        except:
            if (answer == u'0'):
                return cls.encrypt('ERR')
            else:
                return cls.encrypt('ACK')

        try:
            payment = getpaid_models.Payment.objects.get(pk=payment_pk,
                                          status='in_progress',
                                          backend='getpaid.backends.webpaypure')
        except getpaid_models.Payment.DoesNotExist:
            if (answer == u'0'):
                return cls.encrypt('ERR')
            else:
                return cls.encrypt('ACK')

        # create journal entry
        JournalEntry.objects.create(payment=payment, date=datetime.date.today(), body=decrypted_message)

        amount = str(int(payment.amount)) + '00'
        tbk_amount = params['TBK_MONTO']
        same_amount = amount == tbk_amount

        if (answer == u'0'):
            if same_amount and not payment.paid_on:
                payment.on_success()
                return cls.encrypt('ACK')
            else:
                payment.on_failure()
                return cls.encrypt('ERR')
        else:
            payment.on_failure()
            return cls.encrypt('ACK')

    def get_gateway_url(self, request):
        token = self.get_token()

        if self.get_backend_setting('CERTIFIED', False):
            gateway_url = 'https://webpay.transbank.cl:443/cgi-bin/bp_revision.cgi?TBK_VERSION_KCC=6.0&TBK_TOKEN={}'
        else:
            gateway_url = 'https://certificacion.webpay.cl:6443/filtroUnificado/bp_revision.cgi?TBK_VERSION_KCC=6.0&TBK_TOKEN={}'
        
        return gateway_url.format(token), "GET"
