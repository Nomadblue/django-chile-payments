# PayPal backend

This backend handles payment processing via [PayPal](https://paypal.com) using [django-paypal](https://pypi.python.org/pypi/django-paypal/0.1.2).

All the work required to process PayPal payments is done by `django-paypal`. This backend only provides a thin wrapper for integration with django-chile-payments.

## Setup

Make sure you have added django-paypal and this backend to `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'paypal.standard',
        'paypal.standard.ipn',
        'paypal.pro',
        ...
        'getpaid.backends.paypal',
        ...
    )

Add this backend to `GETPAID_BACKENDS`:

    GETPAID_BACKENDS = (...
                        'getpaid.backends.paypal',
                        ...
    )

And configure `django-paypal` with your PayPal credentials:

    # PayPal
    PAYPAL_TEST = True
    PAYPAL_WPP_USER = 'sample_test_user1.example.com'
    PAYPAL_WPP_PASSWORD = 'yourpassword'
    PAYPAL_WPP_SIGNATURE = 'yourwppsignature'
    PAYPAL_RECEIVER_EMAIL = 'receiver@email.com'

## Reference

You can read the full `django-paypal` documentation on [GitHub](https://github.com/spookylukey/django-paypal).