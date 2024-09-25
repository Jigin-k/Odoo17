# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import pprint
from werkzeug import urls

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons2.payment_payu.controllers.main import PayUController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Mollie-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        first_name, last_name = payment_utils.split_partner_name(
            self.partner_id.name)
            api_url = 'https://test.payu.in/_payment'
            payu_values = {
                'key': self.provider_id.payu_merchant_key,
                'txnid': self.reference,
                'amount': self.amount,
                'productinfo': self.reference,
                'firstname': first_name,
                'lastname': last_name,
                'email': self.partner_email,
                'phone': self.partner_phone,
                'return_url': urls.url_join(self.get_base_url(), PayUController._return_url),
                'api_url': api_url,
            }
            payu_values['hash'] = self.provider_id._payu_generate_sign(
                payu_values, incoming=False,
            )



        payload = self._mollie_prepare_payment_request_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._payu_make_request('/payments', data=payload)

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')

        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Mollie and query parameters are provided.
        checkout_url = payment_data['_links']['checkout']['href']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    # def _get_specific_rendering_values(self, payu_values):
    #     """ Override of payment to return Payumoney-specific rendering values.
    #
    #     Note: self.ensure_one() from `_get_processing_values`
    #
    #     :param dict processing_values: The generic and specific processing values of the transaction
    #     :return: The dict of provider-specific processing values
    #     :rtype: dict
    #     """
    #     res = super()._get_specific_rendering_values(payu_values)
    #     if self.provider_code != 'payu':
    #         return res
    #
    #     first_name, last_name = payment_utils.split_partner_name(self.partner_id.name)
    #     api_url = 'https://test.payu.in/_payment'
    #     payu_values = {
    #         'key': self.provider_id.payu_merchant_key,
    #         'txnid': self.reference,
    #         'amount': self.amount,
    #         'productinfo': self.reference,
    #         'firstname': first_name,
    #         'lastname': last_name,
    #         'email': self.partner_email,
    #         'phone': self.partner_phone,
    #         'return_url': urls.url_join(self.get_base_url(), PayUController._return_url),
    #         'api_url': api_url,
    #     }
    #     payu_values['hash'] = self.provider_id._payu_generate_sign(
    #         payu_values, incoming=False,
    #     )
    #     print(payu_values)
    #     return payu_values
    #
    #
    # def _get_tx_from_notification_data(self, provider_code, notification_data):
    #     """ Override of payment to find the transaction based on Payumoney data.
    #
    #     :param str provider_code: The code of the provider that handled the transaction
    #     :param dict notification_data: The notification data sent by the provider
    #     :return: The transaction if found
    #     :rtype: recordset of `payment.transaction`
    #     :raise: ValidationError if inconsistent data were received
    #     :raise: ValidationError if the data match no transaction
    #     """
    #     tx = super()._get_tx_from_notification_data(provider_code, notification_data)
    #     if provider_code != 'payumoney' or len(tx) == 1:
    #         return tx
    #
    #     reference = notification_data.get('txnid')
    #     if not reference:
    #         raise ValidationError(
    #             "PayUmoney: " + _("Received data with missing reference (%s)", reference)
    #         )
    #
    #     tx = self.search([('reference', '=', reference), ('provider_code', '=', 'payumoney')])
    #     if not tx:
    #         raise ValidationError(
    #             "PayUmoney: " + _("No transaction found matching reference %s.", reference)
    #         )
    #
    #     return tx
    #
    # def _process_notification_data(self, notification_data):
    #     """ Override of payment to process the transaction based on Payumoney data.
    #
    #     Note: self.ensure_one()
    #
    #     :param dict notification_data: The notification data sent by the provider
    #     :return: None
    #     """
    #     super()._process_notification_data(notification_data)
    #     if self.provider_code != 'payumoney':
    #         return
    #
    #     # Update the provider reference.
    #     self.provider_reference = notification_data.get('payuMoneyId')
    #
    #     # Update the payment method
    #     payment_method_type = notification_data.get('bankcode', '')
    #     payment_method = self.env['payment.method']._get_from_code(payment_method_type)
    #     self.payment_method_id = payment_method or self.payment_method_id
    #
    #     # Update the payment state.
    #     status = notification_data.get('status')
    #     if status == 'success':
    #         self._set_done()
    #     else:  # 'failure'
    #         # See https://www.payumoney.com/pdf/PayUMoney-Technical-Integration-Document.pdf
    #         error_code = notification_data.get('Error')
    #         self._set_error(
    #             "PayUmoney: " + _("The payment encountered an error with code %s", error_code)
    #         )
    #
