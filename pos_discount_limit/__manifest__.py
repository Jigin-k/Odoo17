# -*- coding: utf-8 -*-
{
    'name': "Pos Discount ",
    'description': """
Set Discount limit in POS""",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale'],

    'data': [
        'views/res_cofig_setings_views.xml',
        'views/pos_order_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_discount_limit/static/src/js/discount.js"
        ]
    },
}
