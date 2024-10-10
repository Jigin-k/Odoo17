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

    @api.model
    def get_average_expense(self):
        products = self.env['product.product'].search([])
        print(products)
        data = {}
        for product in products:
            if product.standard_price > 0:
                data.update({product.name: product.standard_price})
        print(data)
        return data
class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def get_stock_moves(self):
        query = ('''select stock_location.name, count(stock_move.id) from stock_move 
                inner join stock_location on stock_move.location_id = stock_location.id where stock_move.state = 'done' 
                group by stock_location.name''')
        self._cr.execute(query)
        stock_move = self._cr.dictfetchall()
        count = []
        name = []
        for record in stock_move:
            count.append(record.get('count'))
            name.append(record.get('complete_name'))
        value = {'name': name, 'count': count}
        print(value)
        return value
