# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order')
    not_ship_yet_picking = fields.Boolean(string='Not Shipped Yet', related='sale_id.not_ship_yet')