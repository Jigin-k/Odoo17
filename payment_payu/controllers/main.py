# -*- coding: utf-8 -*-
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
        request.env['payment.transaction'].sudo()._handle_notification_data('payu', data)
        return request.redirect('/payment/status')


