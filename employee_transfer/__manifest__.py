# -*- coding: utf-8 -*-
{
    'name': "Transfers",


    'description': """
                   Employee Transfers 
                   """,

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],


    'data': [
'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_transfer_views.xml',
    ],
}

