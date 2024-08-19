import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError

reg_ex = r'^(?=(?:[^A-Za-z]*[A-Za-z]){3})(?=(?:[^\d]*\d){3})(?=(?:[^\W_]*[\W_]){2})[A-Za-z\d\W_]{8}$'

class ResPartner(models.Model):
    _inherit = 'res.partner'

    subscription_account_id = fields.Char(string='Account ID', copy=False, required=True)
    establishment_id = fields.Char('Establishment ID')

    @api.model_create_multi
    def create(self, vals_list):
        """"""
        for vals in vals_list:
            if vals.get('subscription_account_id', " ") == " ":
                vals['order_id'] = self.env['ir.sequence']
        return super(ResPartner, self).create(vals_list)

    @api.constrains('subscription_account_id')
    def validate_account_id(self):
        if self.subscription_account_id:
            match = re.match(reg_ex, self.subscription_account_id)
            if match is None:
                raise ValidationError('Not a valid Account ID')