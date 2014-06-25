# Webpay backend

This backend can handle payment processing via Chilean money broker [Webpay](https://www.transbank.cl/public/pagina_producto_11.html).

## Prerequisites

From your Transbank KCC, get your CGI binaries ready, as we will need them in our project deployment:

* `tbk_bp_pago.cgi`
* `tbk_bp_resultado.cgi`
* `tbk_check_mac.cgi`

Webpay accepts payments in `USD` and `CLP`. Note that you will need to pass certification for each currency you want to support.

## Setup

In order to start working with Webpay you will need to have an activated account with Webpay. An active Webpay account is assigned a unique commerce ID. To get it you must pass through a certification process.

Your `GETPAID_BACKENDS_SETTINGS` must include a 'getpaid.backends.webpay' key which, in turn, must be configured with some mandatory keys for testing environments (called "certificación" in spanish by Transbank) and additionally with some non-mandatory ones (for production environments).

Required keys for certification environment:

* `ASSETS_DIR`: a directory where you have copied the Transbank binaries
* `STATIC_INBOUND_IP`: the ip of your server

Additional required keys for production environment:

* `CERTIFIED`: set this to `True` if you are in a production environment
* `COMMERCE_ID_CLP`: the unique id assigned to you by Transbank, for chilean pesos
* `COMMERCE_ID_USD`: the unique id assigned to you by Transbank, for american dollars
* `TRANSBANK_PUBLIC_KEY`: the public key provided to you by Transbank
* `COMMERCE_PRIVATE_KEY`: your private key

A full example for a production environment:

    GETPAID_BACKENDS_SETTINGS = {
        'getpaid.backends.webpay': {
            'ASSETS_DIR': os.path.join(BASE_DIR, 'assets'),
            'STATIC_INBOUND_IP': '123.123.123.123',
            'CERTIFIED': True,
            'COMMERCE_ID_CLP': '527025007976',
            'COMMERCE_ID_USD': '527026003984',
            'TRANSBANK_PUBLIC_KEY': os.environ.get('TRANSBANK_PUBLIC_KEY'),
            'COMMERCE_PRIVATE_KEY': os.environ.get('COMMERCE_PRIVATE_KEY'),
        }
    }

## The binaries

When you decide to work with Webpay, Transbank gives you a zip with a set of files. The exact files you receive depend on your server's platform and architecture. That set of files are the KCC (means "Kit de Conexion al Comercio") which sits in your server and communicates with Transbank's servers.

The main files of the KCC are three binaries (for Linux 64-bit):

### tbk_pago.cgi

This binary receives a POST from the user's browser with the associated payment data. The POST params are:

* `TBK_MONTO`: The amount of the transaction, plus two extra zeros.
* `TBK_TIPO_TRANSACCION`: The type of the current transaction. Default value is `TR_NORMAL`.
* `TBK_ORDEN_COMPRA`: The order id.
* `TBK_ID_SESION`: The session id. We currently use it to refer to the `Payment` model's id.
* `TBK_URL_EXITO`: The URL to redirect the user if the transaction is successful.
* `TBK_URL_FRACASO`: The URL to redirect the user if the transaction is unsuccessful.

### tbk_resultado.cgi

This binary receives a POST request from Transbank's servers. The data is encrypted and signed.

### tbk_check_mac.cgi

This executable checks the signature on the POST data that `tbk_resultado.cgi` puts on your closing view. It returns the string `CORRECTO` if the test passes or it may crash otherwise (I'm serious).

The rest are text files which configure the environment to run those binaries. They are recreated for each execution by `webpay_run`, a context processor written for this specific purpose.

## Logging

Webpay binaries write logs to disk, given that PaaS providers don't let you write to disk, or the storage is volatile, this backend collects the logs in two django models: `LogEntry` and `JournalEntry`.

Later, to conclude the certification process, you need to provide these logs to Transbank. Both models have a date field that you can use to retrieve the ones you need to submit:

    # Build the event log for today (TBK_EVN<year><month><day>.log)
    >>> "\n".join(map(unicode, LogEntry.objects.filter(date=datetime.date.today())))

    # Build the journal for today (tbk_bitacora_TR_NORMAL_<month><day>.log)
    >>> "\n".join(map(unicode, JournalEntry.objects.filter(date=datetime.date.today())))

This backend stores the log data in the database for convenience.

## A Note About Memory Usage

The `webpay_run` context manager uses `subproccess.Popen` to run the binaries. This should pose no problems normally, but if your website traffic is unusually high, keep in mind that `Popen` forks the current process and, even if the running binary uses only a few KB of memory, uses the same amount of memory
of the parent process.

## Templates

You need to override two templates: the success template (`getpaid/success.html`) and the failure template (`getpaid/failure.html`). Sample templates are provided, but you must make sure that your own templates pass certification.

The context provided for the success view is:

* `payment_items`: A dict with all order items and its prices.
* `order`: The order object.
* `site_url`: The URL of your site.
* `customer_name`: The customer's name.
* `order_id`: The order id.
* `payment_type`: Payment type, according to Transbank's manual.
* `installment_type`: Installments type, according to Transbank's manual.
* `last_digits`: Last 4 digits of the card used in the transaction.
* `transaction_date`: The transaction's date.
* `authorization_code`: Transbank's authorization code. If the transaction is approved, it will be assigned an authorization code.
* `amount`: The current transaction amount.
* `installments`: The number of installments for this payment.

## About your static IP

If you deploy your project to a PaaS provider, like Heroku, you will need a proxy server with a static ip address for receiving requests from Transbank. Currently, the KCC configuration does not accept a domain name as the address of your application server.

You can setup Apache or Nginx to forward Transbank's requests to your server. An minimal configuration example for Nginx:

    # on your server section
    location / {
        proxy_pass http://your.domain.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host your.domain.com;
    }
