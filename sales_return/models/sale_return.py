# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleReturn(models.Model):
    _name = 'sale.return'
    _inherit = ['portal.mixin']
    _rec_name = "name"
    _order = "name"
    _description = "Return Order"


    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('sale.return')

    name = fields.Char(string="Name", default=_get_default_name,
                       help='Name of return order')
    product_id = fields.Many2one('product.product', string="Product Variant",
                                 required=True)
    sale_order = fields.Many2one('sale.order', string="Sale Order",
                                 required=True)
    partner_id = fields.Many2one('res.partner', related='sale_order.partner_id' , string="Customer")
    user_id = fields.Many2one('res.users', string="Responsible",
                              default=lambda self: self.env.user)
    create_date = fields.Datetime(string="Create Date")
    quantity = fields.Float(string="Quantity", default=0)