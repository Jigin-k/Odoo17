{
    'name': "Recurring Subscription",
    'sequence': '-10',
    'version': '17.0.1.0.0',
    'depends': ['base', 'sale', 'crm', 'mail', 'contacts','website'],
    #     'author': "Author Name",
    #     'category': 'Category',
    'description': """
    """,
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/order_wizard_views.xml",
        "wizard/credit_wizard_views.xml",
        "views/subscription_order_views.xml",
        "report/ir.actions.report.xml",
        "report/subscription_order_templates.xml",
        "report/subscription_credit_templates.xml",
        "views/subscription_credit_views.xml",
        "views/subscription_bill_views.xml",
        "views/subscription_action_views.xml",
        "views/res_partner_views.xml",
        "views/crm_lead_views.xml",
        "data/ir_sequence_data.xml",
        "data/ir_cron_data.xml",
        "data/subscription_template_data.xml",
        "data/product_template_data.xml",
"data/subscription_website_templates.xml",
        "views/subscription_website_views.xml",


    ],
    'assets': {
        'web.assets_backend': [
            "recurring_subscription/static/src/js/**"
        ]},
    'installable': True,
    'application': True
}
