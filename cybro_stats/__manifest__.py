{
    'name': 'Cybrosys Statistics',
    'version': '18.0.1.0.0',
    'summary': """ Cybrosys Statistics""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/cybro_stats_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cybro_stats/static/src/xml/dashboard_views.xml',
            'cybro_stats/static/src/js/dashboard.js',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    # 'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
