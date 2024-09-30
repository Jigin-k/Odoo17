# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: PayU',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    'sequence': -1,
    'summary': "",
    'description': " ",
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_payu_templates.xml',

        'data/payment_provider_data.xml',
        'data/account_payment_method.xml',
    ],
    'license': 'LGPL-3',
}
