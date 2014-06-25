from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^pago/(?P<pk>\d+)/$', 'getpaid.backends.webpay.views.pago', name='getpaid-webpay-pago'),
    url(r'^resultado/(?P<pk>\d+)/$', 'getpaid.backends.webpay.views.resultado', name='getpaid-webpay-resultado'),
    url(r'^close/$', 'getpaid.backends.webpay.views.close', name='getpaid-webpay-close'),
    url(r'^success/$', 'getpaid.backends.webpay.views.success', name='getpaid-webpay-success'),
    url(r'^failure/$', 'getpaid.backends.webpay.views.failure', name='getpaid-webpay-failure'),
)
