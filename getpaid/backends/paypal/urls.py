from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^payment/authorization/(?P<pk>[0-9]+)/$', 'getpaid.backends.paypal.views.authorization', name='getpaid-paypal-authorization'),
)
