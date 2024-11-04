# -*- coding: utf-8 -*-
{
    'name': 'Avg Landed Cost',
    'sequence': -1,
    'summary': "",
    'description': " ",
    'depends': ['base','purchase','stock','stock_landed_costs'],
    'data': [
        "security/ir.model.access.csv",
        "views/landed_cost_views.xml",
    ],
}