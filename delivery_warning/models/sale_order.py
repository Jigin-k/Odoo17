# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DeliveryWarning(models.Model):
    _inherit = 'sale.order'

    not_ship_yet = fields.Boolean('Not Shipped Yet')

