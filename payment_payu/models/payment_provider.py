# -*- coding: utf-8 -*-

import hashlib
from odoo import fields,models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', "PayU")],
        ondelete={'payu': 'set default'})
    payu_merchant_key = fields.Char(
        string="Merchant Key",
        help="The key solely used to identify the account with PayU ",
        required_if_provider='payu')
    payu_merchant_salt = fields.Char(
        string="Merchant Salt", required_if_provider='payu',
        groups='base.group_system')

    def _payu_generate_sign(self, values):
        """ Generate the hash for  communications."""
        print(values['txnid'])

        hash_string = f"{self.payu_merchant_key}|{values['txnid']}|{values['amount']}|{values['productinfo']}|{values['firstname']}|{values['email']}|||||||||||{self.payu_merchant_salt}"
        hash = hashlib.sha512(hash_string.encode()).hexdigest()
        print(hash)
        return hash




