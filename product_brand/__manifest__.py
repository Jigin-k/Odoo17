# -*- coding: utf-8 -*-
{
    'name': "Prodcut Brand",
    'description': """
Product Brand On POS""",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale','product'],

    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "product_brand/static/src/xml/order_line_inherit.xml"
        ]
    },
}
