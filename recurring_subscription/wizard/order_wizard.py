# -*- coding: utf-8 -*-

from odoo import fields, models


class RejectionWizard(models.TransientModel):
    _name = 'order.wizard'
    _description = 'Subscription Order Wizard'

    subscription_ids = fields.Many2many("subscription.order",
                                        string="Subscription")
    period = fields.Selection(
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                   ('monthly', 'Monthly'),
                   ('yearly', 'Yearly'), ('custom', 'Custom Dates')],
        string="Period", default="daily", required=True)
    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")

    def action_done(self):
        data = {
            'subscription_ids': self.subscription_ids.ids,
            'period': self.period,
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        print(data)
        return self.env.ref(
            'recurring_subscription.action_report_subscription_order').report_action(
            None, data=data)