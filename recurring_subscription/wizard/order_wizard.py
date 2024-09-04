# -*- coding: utf-8 -*-

from odoo import fields, models


class OrderWizard(models.TransientModel):
    _name = 'order.wizard'
    _description = 'Subscription Order Wizard'

    subscription_ids = fields.Many2many("subscription.order", string="Subscription")
    period = fields.Selection(
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                   ('monthly', 'Monthly'),
                   ('yearly', 'Yearly')], string="Period")

    def action_done(self):
        data = {
            'subscription_ids' : self.subscription_ids.ids,
            'period':self.period
        }
        print(data)
        return self.env.ref('recurring_subscription.action_report_subscription_order').report_action(None,data=data)
        
