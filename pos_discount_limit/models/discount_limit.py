# -*- coding: utf-8 -*-
from odoo import fields, models

class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_discount_limit = fields.Boolean(related='pos_config_id.discount_limit', readonly=False)
    pos_amount_discount_limit = fields.Float(related='pos_config_id.amount_discount_limit', readonly=False)


class DiscountPos(models.Model):
    _inherit = 'pos.config'

    discount_limit = fields.Boolean("Set Discount Limit")
    amount_discount_limit = fields.Float("Maximum Discount Amount")




