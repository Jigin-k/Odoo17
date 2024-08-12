from odoo import fields, models


class Doctors(models.Model):
    _inherit = "hr.employee"
    _description = "Doctors"

    qualification = fields.Char(string="Qualification")
    age = fields.Integer(string="Age")
    fees = fields.Integer(string='Fees')
