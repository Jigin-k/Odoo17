# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeTransfer(models.Model):
    _name = "employee.transfer"
    _description = "Employee Transfer"
    _inherit = "mail.thread"

    employee_id = fields.Many2one("res.partner", "Employee ", store=True,
                                  readonly=False, tracking=True, required=True)
    company_id = fields.Many2one('res.company', 'Current Company',
                                 default=lambda self: self.env.company)
    request_date = fields.Date("Date", default=fields.Date.today())
    to_company_id = fields.Many2one('res.company', "To Company", required=True,
                                    domain="[('id', '!=', company_id)]")
    reason = fields.Text('Reason', required=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')], string='Status', required=True,
        tracking=True, copy=False, default='draft')
    rejection_reason = fields.Text('Rejected Reason')

    def action_send_request(self):
        self.state = 'to_approve'

    def action_reject(self):
        """Open the rejection reason wizard """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rejection Reason',
            'view_mode': 'form',
            'res_model': 'rejection.wizard',
            'target': 'new',
        }

    def action_approve(self):
        self.state = 'approved'
        self.employee_id.company_id = self.to_company_id

    # def default_get(self, default_fields):
    #     res = super(EmployeeTransfer, self).default_get(default_fields)
    #     # if not res.get('pick_id') and self._context.get('active_id'):
    #     res['pick_id'] = self._context['active_id']
    #     return res
