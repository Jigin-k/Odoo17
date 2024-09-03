# -*- coding: utf-8 -*-
{
    'name': "single_invoice",
    'description': """
single invoice for multiple sales order    """,
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    'data': [
        'views/account_move_custom_views.xml',
    ]
}

