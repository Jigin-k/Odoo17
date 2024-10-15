# -*- coding: utf-8 -*-

from odoo import api, models


class StockPicking(models.Model):
    """stock picking inherited model"""
    _inherit = 'stock.picking'

    @api.model
    def get_inventory_tiles_data(self, admin):
        """ Return the inventory tile data"""
        domain = [] if admin else [('user_id', '=', self.env.user.id)]

        operations = {
            'incoming_operations': self.search_count(
                domain + [('picking_type_id.code', '=', 'incoming'),
                          ('state', 'not in',
                           ['done', 'cancel'])]),
            'outgoing_operations': self.search_count(
                domain + [('picking_type_id.code', '=', 'outgoing'),
                          ('state', 'not in',
                           ['done', 'cancel'])]),
            'internal_transfers': self.search_count(
                domain + [('picking_type_id.code', '=', 'internal'),
                          ('state', 'not in',
                           ['done', 'cancel'])])}
        return operations

    @api.model
    def get_locations(self):
        """ Returns locations and on-hand product
        quantities."""
        query = ('''select stock_location.name,sum(quantity) as quantity from stock_quant
                        inner join stock_location on stock_quant.location_id = stock_location.id
                        group by stock_location.name''')
        self._cr.execute(query)
        location_onhand = self._cr.dictfetchall()
        value = {}
        print(location_onhand)
        for record in location_onhand:
            value.update({record['name']: record['quantity']})
        return value

    @api.model
    def get_average_expense(self):
        """ Returns Product and its cost"""
        products = self.env['product.product'].search([])
        data = {}
        for product in products:
            if product.standard_price > 0:
                data.update({product.name: product.standard_price})
        return data


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def get_stock_moves(self):
        """
        returns location wise stock moves
        """
        query = (f'''select stock_location.name, count(stock_move.id) from stock_move 
                inner join stock_location on stock_move.location_id = stock_location.id where stock_move.state = 'done'
                group by stock_location.name''')
        print(query)
        self._cr.execute(query)
        stock_move = self._cr.dictfetchall()
        count = []
        name = []
        for record in stock_move:
            count.append(record.get('count'))
            name.append(record.get('name'))
        value = {'name': name, 'count': count}
        return value

    @api.model
    def get_filter_product_moves(self,admin,filter_type):
        """
        returns data based on filter in the chart
        """
        print(admin,"get_filter_product_moves")
        time_filter = ''
        if filter_type == 'this_week':
            time_filter = "EXTRACT('WEEK' FROM stock_move.date) = EXTRACT('WEEK' FROM CURRENT_DATE)"
        elif filter_type == 'this_month':
            time_filter = "EXTRACT('MONTH' FROM stock_move.date) = EXTRACT('MONTH' FROM CURRENT_DATE)"
        elif filter_type == 'this_year':
            time_filter = "EXTRACT('YEAR' FROM stock_move.date) = EXTRACT('YEAR' FROM CURRENT_DATE)"

        user_filter = ''
        if admin == False:
            user_filter = f"AND stock_move.create_uid = {self.env.uid}"

        query = (f'''select product_template.name->>'en_US' as name, 
               sum(product_uom_qty) as total_quantity
        from stock_move
		inner join stock_picking on stock_move.picking_id = stock_picking.id
		inner join stock_picking_type on stock_picking.picking_type_id = stock_picking_type.id
        inner JOIN product_product 
            on stock_move.product_id = product_product.id
        inner JOIN product_template 
            on product_product.product_tmpl_id = product_template.id
			where {time_filter}{user_filter}
        group by product_template.name->>'en_US'
        order by total_quantity DESC''')
        print(query)
        self._cr.execute(query)
        products_quantity = self._cr.dictfetchall()
        quantity = []
        name = []
        for record in products_quantity:
            quantity.append(record.get('total_quantity'))
            name.append(record.get('name'))
        value = {'name': name, 'count': quantity}
        return value



class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    @api.model
    def get_product_moves(self,admin):
        """
        return all the product moves
        """
        user_filter = ''
        if admin == False:
            user_filter = f"AND stock_move_line.create_uid = {self.env.uid}"

        query = (f'''select product_template.name->>'en_US' as name, 
       sum(stock_move_line.quantity)as total_quantity from stock_move_line
       inner join product_product ON stock_move_line.product_id = product_product.id
       inner join product_template ON product_product.product_tmpl_id = product_template.id {user_filter}
       group by product_template.name->>'en_US' order by total_quantity DESC;''')
        self._cr.execute(query)
        products_quantity = self._cr.dictfetchall()
        quantity = []
        name = []
        for record in products_quantity:
            quantity.append(record.get('total_quantity'))
            name.append(record.get('name'))
        value = {'name': name, 'count': quantity}
        return value

class StockValuationLayer(models.Model):

    _inherit = "stock.valuation.layer"

    @api.model
    def get_stock_value(self):
        """
        returns stock valuation data
        """
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
        return result