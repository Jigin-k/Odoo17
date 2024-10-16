# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id.is_only_ordered:
             return {'domain':{'sale_order_line.product_template_id':[('invoice_policy', '=','order')]}}



    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order._create_invoices()
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        print(vals)
        sale_order = self.env['sale.order'].search([('id','=',vals['order_id'])])
        customer = sale_order.partner_id
        if customer.is_only_ordered:
            product = self.env['product.product'].search([('id','=',vals['product_id'])])
            if product.invoice_policy != 'order':
                raise UserError("Products with policy ordered quantity can be ")
        return super(SaleOrderLine, self).create(vals)
