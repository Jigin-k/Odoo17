# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SaleReturn(models.Model):
    _name = 'sale.return'
    _inherit = ['portal.mixin']
    _rec_name = "name"
    _order = "name"
    _description = "Return Order"


    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('sale.return')

    name = fields.Char(string="Name", default=_('New'),
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

    @api.model_create_multi
    def create(self, vals_list):
        """
        To create new sequence for order id
        """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.return') or _('New')
        return super(SaleReturn, self).create(vals_list)