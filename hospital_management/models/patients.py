from odoo import fields,models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Hospital_Management"

    age = fields.Integer(string="Age")
    dob = fields.Date(string="Date Of Birth")
    blood_group = fields.Selection(selection=[('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'),
                                              ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'),
                                              ('o+', 'O+'), ('o-', 'O+')], string='Blood Group')




