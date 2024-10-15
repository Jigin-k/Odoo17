# -*- coding: utf-8 -*-
{
    'name': 'Inventory Dashboard ',
    'category': 'Warehouse',
    'description': """""",
    'author': 'Jigin',
    'depends': ['stock', 'base', 'web','stock_account'],
    'data': [
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_dashboard/static/src/xml/inventory_dashboard.xml',
            'inventory_dashboard/static/src/js/dashboard.js',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
