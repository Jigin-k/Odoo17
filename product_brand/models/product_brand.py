# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Pos Brand'

    name = fields.Char('Brand Name')