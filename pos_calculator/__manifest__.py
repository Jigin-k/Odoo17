# -*- coding: utf-8 -*-
{
    'name': "POS Calculator",
    'description': """POS Calculator""",
    'depends': ['base', 'point_of_sale', 'sale', 'stock', 'account'],

    'data': [
        'views/res_cofig_setings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            "pos_calculator/static/src/xml/calculator_button_views.xml",
            "pos_calculator/static/src/xml/calculator_popup.xml",
            "pos_calculator/static/src/xml/calculator_numpad.xml",
            "pos_calculator/static/src/js/calculator_popup.js",
            "pos_calculator/static/src/js/calculator.js",
            "pos_calculator/static/src/js/calculator_buttons.js",
        ],
        # 'point_of_sale.assets_prod': [
        #     "pos_calculator/static/src/app/calculator_popup.xml",
        #     "pos_calculator/static/src/app/calculator_popup.js",
        # ]
    },
}
