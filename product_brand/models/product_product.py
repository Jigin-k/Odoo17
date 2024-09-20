# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_brand = fields.Many2one("product.brand","Brand")