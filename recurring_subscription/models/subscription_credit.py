# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils


class SubscriptionCredit(models.Model):
    _name = "subscription.credit"
    _description = "Subscription Credit"
    _inherit = "mail.thread"

    name = fields.Char(string="Subscription Name", related="establishment_id.name", readonly=False)
    partner_id = fields.Many2one("res.partner", string="Customer", related="establishment_id.partner_id",
                                 readonly=False)
    credit_amount = fields.Integer(string="Credit Amount", related="establishment_id.recurring_price", readonly=False)
    start_date = fields.Date('Start Date', related="establishment_id.order_date")
    end_date = fields.Date(string='End Date', related="establishment_id.next_billing")
    product_id = fields.Many2one("product.template", string="Product", related="establishment_id.product_id")
    company_id = fields.Many2one("res.company", string="Company ID", related="establishment_id.company_id")
    establishment_id = fields.Many2one("subscription.order", string='Establishment ID')
    due_date = fields.Date(string='Due Date', related="establishment_id.due_date")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('first_approved', 'First Approved'),
        ('fully_approved', 'Fully Approved'),
        ('rejected', 'Rejected')
    ], string='Status', clickable=True, tracking=True)

    @api.onchange('start_date')
    def _onchange_new_date(self):
        for rec in self:
            if rec.start_date:
                rec.end_date = date_utils.add(rec.start_date, days=15)

    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        if self.credit_amount and self.establishment_id:
            if self.credit_amount > self.establishment_id.recurring_price:
                self.establishment_id = False

