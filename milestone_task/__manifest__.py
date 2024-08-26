{
    'name': "Milestone Task",
# 'version': '1.0',
    'depends': ['base', 'sale','project'],
#     'author': "Author Name",
#     'category': 'Category',
    'description': """
    good Module 
    """,
    # data files always loaded at installation
    'data': [
    "views/sale_order_custom_views.xml",
    "views/sale_order_line_custom_views.xml"
    ],
 'installable':True,
}
