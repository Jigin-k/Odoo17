# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hmac
import logging
import pprint

from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayUController(http.Controller):
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def payu_return_from_checkout(self, **data):
        """ Process the notification data sent by PayUmoney after redirection from checkout.
        """
        _logger.info("handling redirection from PayU money with data:\n%s", pprint.pformat(data))
        print("controller",data)

        # Check the integrity of the notification
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'payu', data
        )
        print(tx_sudo,"txxxxxxx")
        self._verify_notification_signature(data, tx_sudo)
        print("wwwwww")

        # Handle the notification data
        tx_sudo._handle_notification_data('payu', data)
        return request.redirect('/payment/status')

    @staticmethod
    def _verify_notification_signature(notification_data, tx_sudo):
        """ Check that the received signature matches the expected one.

        :param dict notification_data: The notification data
        :param recordset tx_sudo: The sudoed transaction referenced by the notification data, as a
                                  `payment.transaction` record
        :return: None
        :raise: :class:`werkzeug.exceptions.Forbidden` if the signatures don't match
        """
        # Retrieve the received signature from the data
        received_signature = notification_data.get('hash')
        if not received_signature:
            _logger.warning("received notification with missing signature")
            raise Forbidden()
        print(received_signature)

        # Compare the received signature with the expected signature computed from the data
        expected_signature = tx_sudo.provider_id._payu_generate_sign(
            notification_data, incoming=True
        )
        print(expected_signature)
        if not hmac.compare_digest(received_signature, expected_signature):
            _logger.warning("received notification with invalid signature")
            raise Forbidden()
