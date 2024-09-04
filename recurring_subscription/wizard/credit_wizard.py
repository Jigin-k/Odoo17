 # -*- coding: utf-8 -*-

from odoo import fields, models


class CreditWizard(models.TransientModel):
    _name = 'credit.wizard'
    _description = 'Subscription credit Wizard'

    subscription_ids = fields.Many2many("subscription.order",
                                        string="Subscription")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')])

    def action_done(self):
        print("hi")
        # data = {
        #     'subscription_ids': self.subscription_ids.ids,
        #     'period': self.period
        # }
        # print(data)
        # return self.env.ref(
        #     'recurring_subscription.action_report_subscription_order').report_action(
        #     None, data=data)

