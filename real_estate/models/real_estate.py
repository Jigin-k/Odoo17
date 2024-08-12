from odoo import fields, models


class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate'

    title = fields.Char(required=True, size=40)
    description = fields.Char()
    postcode = fields.Integer()
    expected_price = fields.Integer()
    bed_rooms = fields.Char()
    facades = fields.Char()
    active = fields.Boolean(default=True)
    garbage = fields.Boolean(default=True)
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer(string="Garden Area(SqKm")
    available_from = fields.Date()
    area = fields.Integer()
    selling_price = fields.Integer(readonly=True)
    status = fields.Selection(selection=[('new', 'New'), ('offer recieved', 'Offer Recieved')], string='Status', required=True,)

