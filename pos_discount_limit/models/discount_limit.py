# -*- coding: utf-8 -*-
from odoo import api, fields, models

class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_discount_limit = fields.Boolean(related='pos_config_id.discount_limit', readonly=False)
    pos_amount_discount_limit = fields.Float(related='pos_config_id.amount_discount_limit', readonly=False)


class DiscountPos(models.Model):
    _inherit = 'pos.config'

    discount_limit = fields.Boolean("Set Discount Limit")
    amount_discount_limit = fields.Float("Maximum Discount Amount")

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    discount_amount = fields.Float(string="Discount Amount", compute="_compute_discount_amount")

    @api.depends('qty', 'price_unit', 'discount')
    def _compute_discount_amount(self):
        for rec in self:
            if rec.tax_ids_after_fiscal_position.amount:
                rec.discount_amount = (rec.qty * rec.price_unit * (
                            (rec.tax_ids_after_fiscal_position.amount + 100) / 100)) * (
                                              rec.discount / 100)
            else:
                rec.discount_amount = rec.qty * rec.price_unit * (rec.discount / 100)



class PosOrder(models.Model):
    _inherit = 'pos.order'

    total_discount_amount = fields.Float(string="Total Discount Amount", compute="_compute_total_discount_amount")

    @api.depends('lines')
    def _compute_total_discount_amount(self):
        for rec in self:
            total_discount_amount = 0
            for line in rec.lines:
                total_discount_amount += line.discount_amount
            rec.total_discount_amount = total_discount_amount

    @api.model
    def total_session_discount(self, pos_session_id):
        orders = self.search([('session_id', '=', pos_session_id)])
        total_discount = sum(order.total_discount_amount for order in orders)
        return total_discount





