# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'


    original_amount = fields.Float(compute='_compute_original_amount')

    @api.depends('order_ids')
    def _compute_original_amount(self):
        for order in  self.order_ids:
            print(order)


