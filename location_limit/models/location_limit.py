# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductLocationLimit(models.Model):
    _name = 'location.limit'
    _description = 'Product Location Max Quantity Limit'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    location_id = fields.Many2one('stock.location', string="Location", required=True)
    max_quantity = fields.Float(string="Max Quantity", required=True)



class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.constrains('quantity')
    def _check_max_capacity(self):
        for quant in self:
            location_limit = self.env['location.limit'].search([
                ('product_id', '=', quant.product_id.id),
                ('location_id', '=', quant.location_id.id)
            ], limit=1)

            if location_limit:
                if quant.quantity > location_limit.max_quantity:
                    raise ValidationError(
                        f"On-hand quantity of {quant.product_id.display_name} in "
                        f"{quant.location_id.display_name} exceeds the maximum capacity. "
                    )
