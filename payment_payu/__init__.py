# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.tools import config
from . import models
from . import controllers


from odoo.addons.payment import setup_provider, reset_payment_provider

#
# def pre_init_hook(env):
#     if not any(config.get(key) for key in ('init', 'update')):
#         raise UserError(
#             "This module is deprecated and cannot be installed. "
#             "Consider installing the Payment Provider: Razorpay module instead.")
#
#
# def post_init_hook(env):
#     setup_provider(env, 'payu')
#
#
# def uninstall_hook(env):
#     reset_payment_provider(env, 'payu')