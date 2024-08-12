import re
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


def _validate_establishment_id(est_id):
    reg_ex = r'^(?=(?:[^A-Za-z]*[A-Za-z]){3})(?=(?:[^\d]*\d){3})(?=(?:[^\W_]*[\W_]){2})[A-Za-z\d\W_]{8}$'
    return re.match(reg_ex, est_id) is not None


class SubscriptionCredit(models.Model):
    _name = "subscription.credit"
    _description = "Subscription Credit"
    _inherit = "mail.thread"

    name = fields.Many2one("subscription.order", string="Subscription Name")
    customer_id = fields.Many2one("res.partner", string="Customer", related="establishment_id.customer_id")
    credit_amount = fields.Float(string="Credit Amount", related="establishment_id.recurring_price")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('first approved', 'First Approved'),
        ('fully approved', 'Fully Approved'),
        ('rejected', 'Rejected')
    ], string='Status', clickable=True, tracking=True)
    start_date = fields.Date('Start Date', related="establishment_id.order_date")
    end_date = fields.Date('End Date')
    product_id = fields.Many2one("product.template", string="Product", related="establishment_id.product_id")
    company_id = fields.Char(string="Company ID", related="establishment_id.company_id")
    establishment_id = fields.Many2one("subscription.order", string='Establishment ID')
    due_date = fields.Date(string='Due Date')

    @api.onchange('start_date')
    def _check_change(self):
        if self.start_date:
            self.due_date = self.start_date + timedelta(days=15)

    @api.constrains('establishment_id')
    def _check_establishment_id(self):
        for record in self:
            if record.establishment_id:
                if not _validate_establishment_id(record.establishment_id):
                    raise ValidationError(
                        "Establishment ID contains only 3 alphabets, 3 numbers, and 2 special characters.")

    # @api.onchange('establishment_id')
    # def onchange_model1_id(self):
    #     for rec in self:
    #         return {'domain': {'establishment_id': [('establishment_id', '=', rec.establishment_id.establishment_id)]}}

    # @api.onchange('establishment_id')
    # def _onchange_establishment_id(self):
    #
    #     for rec in self.establishment_id:
    #         self.title = self.establishment_id.name
    #         self.customer_id = self.establishment_id.customer_id
    #         self.credit_amount = self.establishment_id.recurring_price
    #         self.start_date = self.establishment_id.order_date
    #         self.product_id = self.establishment_id.product_id
    #         self.company_id = self.establishment_id.company_id
