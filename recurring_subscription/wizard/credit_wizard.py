# -*- coding: utf-8 -*-

from odoo import fields, models


class CreditWizard(models.TransientModel):
    _name = 'credit.wizard'
    _description = 'Subscription credit Wizard'

    subscription_id = fields.Many2one("subscription.order",
                                      string="Subscription")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')])

    def action_done(self):
        data = {
            'subscription_id': self.subscription_id.id,
            'state': self.state
        }
        print(data)
        return self.env.ref(
            'recurring_subscription.action_report_subscription_credit').report_action(
            None, data=data)
