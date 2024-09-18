# -*- coding: utf-8 -*-
{
    'name': "Pos Discount ",
    'description': """
Set Discount limit in POS""",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale'],

    'data': [
        'views/res_cofig_setings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_frontend': [
            "pos_discount_limit/statis/src/js/discount.js"
        ]
    },
}
