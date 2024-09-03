# -*- coding: utf-8 -*-

from odoo import fields, models


class RejectionWizard(models.TransientModel):
    _name = 'order.wizard'
    _description = 'Subscription Order Wizard'

    subscription = fields.Many2many("subscription.order", string="Subscription")
    period = fields.Selection(
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                   ('monthly', 'Monthly'),
                   ('yearly', 'Yearly')], string="Period")

    def action_done(self):
        print("hi")
