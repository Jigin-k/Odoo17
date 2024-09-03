# -*- coding: utf-8 -*-

from odoo import api, fields, models



class SubscriptionCredit(models.Model):
    _name = "subscription.credit"
    _description = "Subscription Credit"
    _inherit = "mail.thread"

    order_id = fields.Many2one("subscription.order",
                               string="Subscription Name",
                       readonly=False)
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 readonly=False)
    credit_amount = fields.Integer(string="Credit Amount",
                                   readonly=False)
    start_date = fields.Date('Start Date')
    end_date = fields.Date(string='End Date')
    product_id = fields.Many2one("product.product", string="Product")
    company_id = fields.Many2one("res.company", string="Company ID",
                                 related="order_id.company_id")
    title = fields.Char(string='Name')
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('first_approved', 'First Approved'),
        ('fully_approved', 'Fully Approved'),
        ('rejected', 'Rejected')
    ], string='Status', clickable=True, tracking=True)
    bill_id = fields.Many2one("subscription.bill", string="Bills",
                              related="order_id.bill_id")


    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        """
        If credit amount is greater than recurring price all the
         records will bw none.
        """
        if self.credit_amount and self.order_id:
            if self.credit_amount > self.order_id.recurring_price:
                self.order_id = False
