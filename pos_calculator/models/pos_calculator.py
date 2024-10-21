# -*- coding: utf-8 -*-
from odoo import fields, models

class PosCalculator(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_calculator = fields.Boolean(related='pos_config_id.virtual_calculator', readonly=False)


class CalculatorPos(models.Model):
    _inherit = 'pos.config'

    virtual_calculator = fields.Boolean("Enable Virtual Calculator")

