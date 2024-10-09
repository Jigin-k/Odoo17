# -*- coding: utf-8 -*-

from odoo import api, models


class StockPicking(models.Model):
    """stock picking inherited model"""
    _inherit = 'stock.picking'

    @api.model
    def get_inventory_tiles_data(self):
        """ Return the inventory tile data"""
        company_id = self.env.company
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', company_id.id)], limit=1)

        incoming_operations = self.search([('company_id', '=', company_id.id),
                                           ('picking_type_id.code', '=',
                                            'incoming'),
                                           ('state', 'not in',
                                            ['done', 'cancel'])])

        outgoing_operations = self.search([('company_id', '=', company_id.id),
                                           ('picking_type_id.code', '=',
                                            'outgoing'),
                                           ('state', 'not in',
                                            ['done', 'cancel'])])

        internal_transfers = self.search([('company_id', '=', company_id.id),
                                          ('picking_type_id.code', '=',
                                           'internal'),
                                          ('state', 'not in',
                                           ['done', 'cancel'])])
        print(incoming_operations,outgoing_operations,internal_transfers)


        return {
            'incoming_operations': len(incoming_operations),
            'outgoing_operations': len(outgoing_operations),
            'internal_transfers': len(internal_transfers),
        }

    @api.model
    def get_locations(self):
        """ Returns locations and locations that have on-hand product
        quantities."""
        stock_quant_ids = self.env['stock.quant'].search([])
        locations = stock_quant_ids.mapped('location_id')
        value = {}
        for rec in locations:
            loc_stock_quant = stock_quant_ids.filtered(
                lambda x: x.location_id == rec)
            on_hand_quantity = sum(
                loc_stock_quant.mapped('inventory_quantity_auto_apply'))
            value[rec.name] = on_hand_quantity
        print(value)
        return value
