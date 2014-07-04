from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^notify/$', 'getpaid.backends.webpaypure.views.notify', name='getpaid-webpaypure-notify'),
    url(r'^success/$', 'getpaid.backends.webpaypure.views.success', name='getpaid-webpaypure-success'),
    url(r'^failure/$', 'getpaid.backends.webpaypure.views.failure', name='getpaid-webpaypure-failure'),
)
