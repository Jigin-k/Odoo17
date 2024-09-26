# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hmac
import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayUController(http.Controller):
    _return_url = '/payment/payu/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def payumoney_return_from_checkout(self, **data):
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

        # Handle the notification data
        tx_sudo._handle_notification_data('payu', data)
        return request.redirect('/payment/status')