# -*- coding: utf-8 -*-
from odoo import fields,models

class PartnerAccount(models.Model):
    _name = "partner.account"
    _description = "Partner Account"

    account_id = fields.Char(string="Account ID")


    _sql_constraints = [('account_id', 'UNIQUE(account_id)', 'The Account ID must be unique')]