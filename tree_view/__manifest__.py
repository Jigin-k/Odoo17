{
    'name': 'Sale Tree View',
    'sequence': -1,
    'summary': "",
    'description': " ",
    'depends': ['base', 'sale'],
    'data': [
        "views/sales_tree.xml",
    ],
    'assets': {
    'web.assets_backend': [
        'tree_view/static/src/**/*',
    ],
    },
}