# -*- coding: utf-8 -*-
from odoo import models, fields


class StockQuant(models.Model):
   _inherit = 'stock.location'

   max_capacity = fields.Float(string='Max On-Hand Quantity', default=0.0)
   product_id = fields.Many2one('product.template')
