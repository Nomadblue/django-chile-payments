# Workflow

# Your order model

First of all, we must define which model will be representing an item on our shopping cart, subscription, or whatever. Thanks to the design of this app, you can use an new one, a previously defined one you have, or even one from a 3rd party app. There are only a few requirements, which we will define below.

Let's create a minimal model for our explanation purposes:

    from django.db import models
    from django.core.urlresolvers import reverse
    import getpaid


    class Order(models.Model):
        name = models.CharField(max_length=255)
        paid = models.BooleanField(default=False)

        def __unicode__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('order_detail', kwargs={'pk': self.pk})

        @property
        def total(self):
            return 1000

    getpaid.register_to_payment(Order, unique=False, related_name='payments')

From the code above we can state the following:

1. To notify the app, you must register your model through the `getpaid.register_to_payment` signal. This will generate a Payment model class that will store payments with a `ForeignKey` to the original order class. Also, notice that you can pass `ForeignKey` field parameters as keyword args in the signal call.
2. The `__unicode__` method must be defined as it will be used in some parts of the app as a fallback for generating order descriptions.
3. The `get_absolute_url` method also must be defined. It is used again as a fallback for some final redirections after payment success or failure (if you do not provide otherwise).
4. A `total` property must exist, either as a property function or as a model field. Again, the app requires this property in some parts of the code.

## Order form

This example shows how to `post` to initiate the payment process:

    <form action="{% url 'getpaid-new-payment' currency='CLP' %}" method="post">
      {% csrf_token %}
      <input type="hidden" name="order" value="{{ object.pk }}">
      <input type="hidden" name="backend" value="getpaid.backends.webpay">
      <input type="submit" value="Pay">
      </div>
    </form>

This form will redirect the client to an intermediate page with a form with external action attribute. It is recommended to override the template `getpaid/payment_post_form.html` so that you can display a message to the user and also use Javascript to submit the form automatically after page is loaded.

## Signals

`django-chile-payments` is agnostic, so in order to make it know information required to start the payment process, we use the following signal:

    def new_payment_query_listener(sender, order=None, payment=None, **kwargs):
        payment.amount = order.total
        payment.currency = 'CLP'

    getpaid.signals.new_payment_query.connect(new_payment_query_listener)

Signals are also used to inform you that some particular payment just changed status. In this case we use `getpaid.signals.payment_status_changed` signal. For example, in our previous Order model we included a boolean field to store if the order was already paid or not:

    from getpaid import signals

    def payment_status_changed_listener(sender, instance, old_status, new_status, **kwargs):
        """
        Here we will actually do something, when payment is accepted.
        E.g. lets change an order status.
        """
        if old_status != 'paid' and new_status == 'paid':
            # Ensures that we process order only one
            instance.order.paid = True
            instance.order.save()

    signals.payment_status_changed.connect(payment_status_changed_listener)

When the payment status changes from any non 'paid' to 'paid' status, this means that all necessary amount was verified by your payment broker. You have access to your Order object at `instance.order`.

## Configure payment backends

Ready to the next step? **Great**! Go ahead to [configure Webpay backend](/django-chile-payments/webpay) or [PayPal backend](/django-chile-payments/paypal).
