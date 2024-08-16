# -*- coding: utf-8 -*-

from odoo import models, fields


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
    subscription_ids = fields.Many2many("subscription.order",inverse_name='establishment_id', string="Subscriptions")
    total_credit_amount = fields.Float(string="Total Credit Amount")
    subscription_order_ids = fields.One2many("subscription.order", inverse_name='bill_id', string="Subscription Order")


    def subscription_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree',
            'res_model': 'subscription.order',
            'domain': [('bill_id', '=', self.id)],
            'context': "{'create': False}"
        }
