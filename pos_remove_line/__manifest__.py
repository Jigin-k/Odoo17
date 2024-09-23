# -*- coding: utf-8 -*-
{
    'name': "Remove POS Order Line",
    'description': """
Remove line in POS""",
    'version': '17.0.1.0.0',
    'depends': ['base', 'point_of_sale'],

    'data': [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_remove_line/static/src/xml/order_line_inherit.xml",
            "pos_remove_line/static/src/xml/clear_lines.xml",
            "pos_remove_line/static/src/js/orderline.js",
        ],
    },
}
