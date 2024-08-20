# -*- coding: utf-8 -*-
import dateutil.utils

from odoo import api, fields, models


class SubscriptionBill(models.Model):
    _name = "subscription.bill"
    _description = "Subscription Bill"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Scheduled Bill")
    simulation = fields.Boolean(string="Simulation")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    customer_ids = fields.Many2many("res.partner", string="Customers")
    active = fields.Boolean(string="Active", default=True)
    # subscription_ids = fields.Many2many("subscription.order",
    #                                     string="Subscriptions")
    total_credit_amount = fields.Float(string="Total Credit Amount",
                                       compute='_compute_total_credit')
    subscription_order_ids = fields.One2many("subscription.order",
                                             inverse_name='bill_id',
                                             string="Subscription Order")


    def subscription_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree',
            'res_model': 'subscription.order',
            'domain': [('bill_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    @api.depends('subscription_order_ids.recurring_price')
    def _compute_total_credit(self):
        for rec in self:
            rec.total_credit_amount = sum(rec.subscription_order_ids.filtered(
                lambda order: order.state == 'confirm').mapped(
                'recurring_price'))

    def action_create_invoice(self):
        print(self)
        global invoices
        #self.ensure_one()
        invoice_vals_list = []
        for order in self.subscription_order_ids.filtered(
                lambda orders: orders.state == 'confirm'):
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': order.partner_id.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [(0, 0, {
                    'product_id': order.product_id.id,
                    'name': order.name,
                    'quantity': 1,
                    'price_unit': order.recurring_price
                })],
            }
            invoice_vals_list.append(invoice_vals)
            print(invoice_vals)
        if invoice_vals_list:
            self.active = False
            invoices = self.env['account.move'].create(invoice_vals_list)
            # self.env('subscription.order').search([()])



        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('id', 'in', invoices.ids)],
            'context': {'create': False},
        }

    # def scheduled_action_create_invoice(self):
    #     print('hello')

        # if self.end_date:
        #     print('heytrytrereds')
        # if self.end_date < datetime.date.today():
        #     print(datetime.today())
        #     def action_create_invoice():
        #         action_create_invoice()




