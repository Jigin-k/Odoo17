# -*- coding: utf-8 -*-
from odoo import fields,models

class ResPartner(models.Model):
    """stock picking inherited model"""
    _inherit = 'res.partner'

    is_only_ordered = fields.Boolean()
