# -*- coding: utf-8 -*-
{
    'name': "Transfers",

    'description': """
                   Employee Transfers 
                   """,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/rejection_wizard_views.xml',
        'views/employee_transfer_views.xml',

    ],
}
