{
    'name': 'Inventory Dashboard ',
    'version': '17.0.1.0.0',
    'category': 'Warehouse',
    'description': """""",
    'author': 'Jigin',
    'depends': ['stock', 'base','web'],
    'data': [
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_dashboard/static/src/xml/inventory_dashboard.xml',
            'inventory_dashboard/static/src/js/dashboard.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}