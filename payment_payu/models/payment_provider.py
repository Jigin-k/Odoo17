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




    def _payu_generate_sign(self, values, incoming=True):
        """ Generate the shasign for incoming or outgoing communications.

        :param dict values: The values used to generate the signature
        :param bool incoming: Whether the signature must be generated for an incoming (PayU to
                              Odoo) or outgoing (Odoo to PayUMoney) communication.
        :return: The shasign
        :rtype: str
        """
        sign_values = {
            **values,
            'key': self.payu_merchant_key,
            'salt': self.payu_merchant_salt,
        }
        # eOSBtQ
        # YFpoDYncPWJ5uw1gM2k4FIsRZtvHwuVm

        if incoming:
            keys = 'salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|' \
                   'txnid|key'
            sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
        else:  # outgoing
            keys = 'key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt'
            sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
            print("hash",hashlib.sha512(sign.encode('utf-8')).hexdigest())
        return hashlib.sha512(sign.encode('utf-8')).hexdigest()





