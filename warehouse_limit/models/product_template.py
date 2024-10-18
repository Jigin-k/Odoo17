# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    max_on_hand_qty = fields.Float(string='Max On-Hand Quantity', default=0.0)



