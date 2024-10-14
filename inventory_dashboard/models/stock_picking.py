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
            name.append(record.get('name'))
        value = {'name': name, 'count': count}
        print(value)
        return value

    @api.model
    def get_filter_product_moves(self,filter_type):
        time_filter = ''
        if filter_type == 'this_week':
            time_filter = "EXTRACT('WEEK' FROM stock_move.date) = EXTRACT('WEEK' FROM CURRENT_DATE)"
        elif filter_type == 'this_month':
            time_filter = "EXTRACT('MONTH' FROM stock_move.date) = EXTRACT('MONTH' FROM CURRENT_DATE)"
        elif filter_type == 'this_year':
            time_filter = "EXTRACT('YEAR' FROM stock_move.date) = EXTRACT('YEAR' FROM CURRENT_DATE)"

        query = (f'''select product_template.name->>'en_US' as name, 
               sum(product_uom_qty) as total_quantity
        from stock_move
		inner join stock_picking on stock_move.picking_id = stock_picking.id
		inner join stock_picking_type on stock_picking.picking_type_id = stock_picking_type.id
        inner JOIN product_product 
            on stock_move.product_id = product_product.id
        inner JOIN product_template 
            on product_product.product_tmpl_id = product_template.id
			where {time_filter}
        group by product_template.name->>'en_US'
        order by total_quantity DESC''')
        self._cr.execute(query)
        products_quantity = self._cr.dictfetchall()
        quantity = []
        name = []
        for record in products_quantity:
            quantity.append(record.get('total_quantity'))
            name.append(record.get('name'))
        value = {'name': name, 'count': quantity}
        print(value)
        return value



class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    @api.model
    def get_product_moves(self):

        query = ('''select product_template.name->>'en_US' as name, 
       sum(stock_move_line.quantity)as total_quantity from stock_move_line
       inner join product_product ON stock_move_line.product_id = product_product.id
       inner join product_template ON product_product.product_tmpl_id = product_template.id
       group by product_template.name->>'en_US' order by total_quantity DESC;''')
        self._cr.execute(query)
        products_quantity = self._cr.dictfetchall()
        quantity = []
        name = []
        for record in products_quantity:
            quantity.append(record.get('total_quantity'))
            name.append(record.get('name'))
        value = {'name': name, 'count': quantity}
        print(value)
        return value

class StockValuationLayer(models.Model):

    _inherit = "stock.valuation.layer"

    @api.model
    def get_stock_value(self):

        query = ('''select product_template.name->>'en_US' as name,
       sum(stock_valuation_layer.value)as total_value from stock_valuation_layer
       inner join product_product ON stock_valuation_layer.product_id = product_product.id
       inner join product_template ON product_product.product_tmpl_id = product_template.id
       group by product_template.name->>'en_US' order by total_value DESC;''')
        self._cr.execute(query)
        stock_value = self._cr.dictfetchall()
        value = []
        name = []
        for record in stock_value:
            value.append(record.get('total_value'))
            name.append(record.get('name'))
        result = {'name': name, 'stock_value': value}
        print(value)
        return result