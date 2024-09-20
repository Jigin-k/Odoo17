# -*- coding: utf-8 -*-
{
    'name': "Prodcut Brand",
    'description': """
Product Brand On POS""",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale','product'],

    'data': ['security/ir.model.access.csv',
        'views/product_brand_views.xml',
        'views/product_template_views.xml',
        'views/product_brand_menu.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "product_brand/static/src/xml/order_line_inherit.xml",
            "product_brand/static/src/xml/product_widget_inherit.xml",
            "product_brand/static/src/xml/product_card_inherit.xml",

'product_brand/static/src/js/custom_orderline.js',
        ],
'web.assets_backend': [

   ],
    },
}
