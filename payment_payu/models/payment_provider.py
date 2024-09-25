# -*- coding: utf-8 -*-

import hashlib
from odoo import fields,models
import requests
from werkzeug import urls
from odoo.addons.payment_payulatam.const import DEFAULT_PAYMENT_METHODS_CODES


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

    # def _payu_generate_sign(self, values, incoming=True):
    #     """ Generate the shasign for incoming or outgoing communications.
    #
    #     :param dict values: The values used to generate the signature
    #     :param bool incoming: Whether the signature must be generated for an incoming (PayU to
    #                           Odoo) or outgoing (Odoo to PayUMoney) communication.
    #     :return: The shasign
    #     :rtype: str
    #     """
    #     sign_values = {
    #         **values,
    #         'key': self.payu_merchant_key,
    #         'salt': self.payu_merchant_salt,
    #     }
    #     if incoming:
    #         keys = 'salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|' \
    #                'txnid|key'
    #         sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
    #     else:  # outgoing
    #         keys = 'key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt'
    #         sign = '|'.join(f'{sign_values.get(k) or ""}' for k in keys.split('|'))
    #     return hashlib.sha512(sign.encode('utf-8')).hexdigest()



    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return DEFAULT_PAYMENT_METHODS_CODES


    def _payu_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at mollie endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request
        :param dict data: The payload of the request
        :param str method: The HTTP method of the request
        :return The JSON-formatted content of the response
        :rtype: dict
        :raise: ValidationError if an HTTP error occurs
        """
        self.ensure_one()
        endpoint = f'/v2/{endpoint.strip("/")}'
        url = urls.url_join('https://api.mollie.com/', endpoint)

        odoo_version = service.common.exp_version()['server_version']
        module_version = self.env.ref('base.module_payment_mollie').installed_version
        headers = {
            "Accept": "application/json",
            "Authorization": f'Bearer {self.mollie_api_key}',
            "Content-Type": "application/json",
            # See https://docs.mollie.com/integration-partners/user-agent-strings
            "User-Agent": f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
        }

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
                )
                raise ValidationError(
                    "Mollie: " + _(
                        "The communication with the API failed. Mollie gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Mollie: " + _("Could not establish the connection to the API.")
            )
        return response.json()