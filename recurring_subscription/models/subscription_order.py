# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


def _validate_establishment_id(est_id):
    reg_ex = r'^(?=(?:[^A-Za-z]*[A-Za-z]){3})(?=(?:[^\d]*\d){3})(?=(?:[^\W_]*[\W_]){2})[A-Za-z\d\W_]{8}$'
    return re.match(reg_ex, est_id) is not None


class SubscriptionOrder(models.Model):
    _name = "subscription.order"
    _description = "Subscription Order"
    _inherit = ["mail.thread"]
    _rec_name = "establishment_id"

    order_id = fields.Char(string='Order ID', readonly=True, default=_('New'),
                           copy=False)
    name = fields.Char(string='Name', required=True)
    establishment_id = fields.Char(string='Establishment ID', required=True,
                                   copy=False)
    order_date = fields.Date(string="Order Date")
    due_date = fields.Date(string='Due Date')
    next_billing = fields.Date(string="Next Bill Date")
    recurring_price = fields.Integer(string="Recurring Price")
    is_lead = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Customer")
    description = fields.Text(string="Description")
    terms_conditions = fields.Html('Terms And Conditions')
    product_id = fields.Many2one("product.product", string="Product")
    company_id = fields.Many2one("res.company", string="Company ID",
                                 default=lambda self: self.env.company)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string='Status', required=True,
        tracking=True, copy=False, default='draft')
    bill_id = fields.Many2one("subscription.bill", string="Bills")

    @api.model_create_multi
    def create(self, vals_list):
        """
        To create new sequence for order id
        """
        for vals in vals_list:
            if vals.get('order_id', _('New')) == _('New'):
                vals['order_id'] = self.env['ir.sequence'].next_by_code(
                    'subscription.order') or _('New')
        return super(SubscriptionOrder, self).create(vals_list)

    @api.onchange('order_date')
    def _onchange_new_date(self):
        """
           To calculate due date and next billing date based on order date.
        """
        if self.order_date:
            self.next_billing = date_utils.add(self.order_date, months=1)
            self.due_date = date_utils.add(self.next_billing, days=15)

    @api.constrains('establishment_id')
    def _check_establishment_id(self):
        """
            To validate the Establishment ID
        """
        if self.establishment_id:
            if not _validate_establishment_id(self.establishment_id):
                raise ValidationError(
                    "Establishment ID contains exactly 3 alphabets, 3 numbers, and 2 special characters.")

    def action_confirm(self):
        self.update({'state': "confirm"})

    def action_cancel(self):
        self.update({'state': "cancel"})

    @api.onchange('establishment_id')
    def _onchange_establishment_id(self):
        """
        To Auto Populate Partner when partner having corresponding Establishment ID is given.
        """
        partner = self.env['res.partner'].search(
            [('establishment_id', '=', self.establishment_id)], limit=1)
        if partner:
            self.partner_id = partner.id
        else:
            raise ValidationError(
                "No Customer Found With Given Establishment ID")
