{
    'name': 'Inventory Dashboard ',
    # 'version': '18.0.1.0.0',
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
        # "web.chartjs_lib": [
        #     '/web/static/lib/Chart/Chart.js',
        #     '/web/static/lib/chartjs-adapter-luxon/chartjs-adapter-luxon.js',
        # ]

    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
