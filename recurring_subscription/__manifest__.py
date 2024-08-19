{
    'name': "Recurring Subscription",
    'sequence':'-10',
     'version': '17.0.1.0.0',
    'depends': ['base', 'sale', 'crm'],
#     'author': "Author Name",
#     'category': 'Category',
    'description': """
    """,
    'data': [
         "security/ir.model.access.csv",
        "views/subscription_action_views.xml",
        "views/subscription_order_views.xml",
        "views/subscription_credit_views.xml",
        "views/subscription_bill_views.xml",
         "views/res_partner_views.xml",
        "views/crm_lead_views.xml",
        "data/ir_sequence_data.xml"
    ],
'installable':True,
'application': True
}
