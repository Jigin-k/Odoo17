{
    'name': "Hospital Management",
# 'version': '1.0',
    'depends': ['base','contacts','hr'],
#     'author': "Author Name",
#     'category': 'Category',
    'description': """
    good Module 
    """,
    # data files always loaded at installation
    'data': [
         "security/ir.model.access.csv",
        "views/hospital_management_views.xml",
        "views/op_ticket_view.xml",
        "views/patients_view.xml",
        "views/doctors_view.xml",
        "views/consultation_view.xml"
    ],
 'installable':True,
'application': True
}
