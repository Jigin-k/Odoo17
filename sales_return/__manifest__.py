{
    'name': 'Sale Return',
    'sequence': -1,
    'summary': "",
    'description': " ",
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/sale_return_views.xml',
        'views/sale_order_views.xml',

        'data/ir_sequence.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sales_return/static/src/js/sale_return.js'
        ]
    },
}
