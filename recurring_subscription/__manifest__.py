{
    'name': "Recurring Subscription",
    'sequence':'-10',
# 'version': '1.0',
    'depends': ['base','sale'],
#     'author': "Author Name",
#     'category': 'Category',
    'description': """
    """,
    'data': [
         "security/ir.model.access.csv",
        "views/subscription_view.xml",
        "views/order_view.xml",
        "views/credit_view.xml"
    ],
 'installable':True,
'application': True
}
