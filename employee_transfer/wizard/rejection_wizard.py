# -*- coding: utf-8 -*-

from odoo import fields, models


class RejectionWizard(models.TransientModel):
    _name = 'rejection.wizard'
    _description = 'Transfer Rejection Wizard'

    reason = fields.Char("Reason")

    def action_done(self):
        record = self.env['employee.transfer'].browse(
            self._context.get('active_id'))
        record.rejection_reason = self.reason
        record.state = 'rejected'
