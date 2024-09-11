# -*- coding: utf-8 -*-

import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import random, string


def _validate_establishment_id(est_id):
    reg_ex = r'^(?=(?:[^A-Za-z]*[A-Za-z]){3})(?=(?:[^\d]*\d){3})(?=(?:[^\W_]*[\W_]){2})[A-Za-z\d\W_]{8}$'
    return re.match(reg_ex, est_id) is not None


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # subscription_account_id = fields.Char(string='Account ID')
    establishment_id = fields.Char('Establishment ID')
    #
    # @api.model_create_multi
    # def create(self, vals_list):
    #     """
    #     To create partner account ID on partner creation
    #     """
    #     for vals in vals_list:
    #         vals['subscription_account_id'] = ''.join(
    #             (random.choices(string.ascii_letters, k=3) +
    #              random.choices(string.digits, k=3) +
    #              random.choices('!@#$%^&*()', k=2)))
    #     return super(ResPartner, self).create(vals_list)

    @api.constrains('establishment_id')
    def _check_establishment_id(self):
        """
        To validate the Establishment ID
        """
        print(self.establishment_id)
        if self.establishment_id:
            if not _validate_establishment_id(self.establishment_id):
                raise ValidationError(
                    "Establishment ID contains exactly 3 alphabets, 3 numbers, and 2 special characters.")
