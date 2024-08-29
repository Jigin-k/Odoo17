# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    milestone = fields.Integer('Milestone')
    task_id = fields.Many2one('project.task', string="Related Task", ondelete='set null')

    def unlink(self):
        for line in self:
            if line.task_id:
                line.task_id.unlink()

        return super(SaleOrderLine, self).unlink()


