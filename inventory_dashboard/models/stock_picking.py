# -*- coding: utf-8 -*-

from odoo import api, models


class StockMove(models.Model):

    _inherit = "stock.picking"

    @api.model
    def get_operation_types(self):


        stock_picking_type = self.env['stock.picking.type'].search([])
        print(stock_picking_type)
        stock_picking = self.env['stock.picking'].search([])
        print(stock_picking)

        names = []
        num_of_transfer={}
        operation_type_name = {}
        for rec in stock_picking_type:
            names.append(rec.name)
            orders = stock_picking.filtered(lambda r: r.picking_type_id.id == rec.id)
            length_stock_picking = len(orders)
            num_of_transfer.update({rec.id: length_stock_picking})
            operation_type_name.update({rec.id: rec.name})
        return num_of_transfer, operation_type_name



