# django-chile-payments

**Online payments, "the chilean way"**. A django app with a flexible architecture designed to be multi-broker payment processor. Originally developed with love at [Nomadblue](http://www.nomadblue.com).

For now it only sports the *"peso pesado"* of online payments in Chile, an old folk well-known by local developers called [Webpay Plus](https://www.transbank.cl/public/pagina_producto_11.html) from **Transbank**. In the close future, we plan to include other APIs (e.g. [DineroMail](https://cl.dineromail.com/desarrolladores/biblioteca) or [Servipag](https://www.servipag.com/Portal-De-Pagos-En-Linea/Home/botondepago), eventually becoming a de-facto package for Django payment processing in Chile.

Disclaimer: This work has been heavily based from a fork of [django-getpaid](https://github.com/cypreess/django-getpaid), which in turn borrowed a lot of great ideas from another project called **Mamona**.

## Installation

### Source code

The source code of the first stable version will be available on pypi. In the meantime, you can download development version from:

https://github.com/Nomadblue/django-chile-payments.git

### Settings

Add the app (codenamed 'getpaid') to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'getpaid',
        ....
    )

Next, set `GETPAID_BACKENDS` with the webpay backend and add it to `INSTALLED_APPS` as well:

    GETPAID_BACKENDS = ('getpaid.backends.webpay',)
    INSTALLED_APPS += GETPAID_BACKENDS

Now we are going to define the minimum parameters needed for development purposes.

> See [the complete list of keys in the backend documentation](/django-chile-payments/webpay/).

    GETPAID_BACKENDS_SETTINGS = {
        'getpaid.backends.webpay': {
            'ASSETS_DIR': os.path.join('/path/to/your/assets'),
            'STATIC_INBOUND_IP': '123.123.123.123',
        },
    }

We do not like using `contrib.sites` so we use to set a `SITE_URL` that can be changed on each environment. For now, as we are on our local machine, this will suffice:

    SITE_URL = 'http://127.0.0.1:8000'

Enable the app in your urls:

    url(r'', include('getpaid.urls')),

Run `./manage.py syncdb` in order to create additional database tables.

## Connect your project

Ready to the next step? **Great**! Go ahead to [connect django-chile-payments with your project](/django-chile-payments/workflow).
