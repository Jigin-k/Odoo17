# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeTransfer(models.Model):
    _name = "employee.transfer"
    _description = "Employee Transfer"
    _inherit = "mail.thread"


    employee_id = fields.Many2one("res.partner","Employee Name",store=True, readonly=False, tracking=True, required=True)
    company_id = fields.Many2one('res.company', 'Current Company', default=lambda self: self.env.company)
    request_date = fields.Date("Date",default = fields.Date.today())
    to_company_id = fields.Many2one('res.company',"To Company", required=True)
    reason = fields.Text('Reason')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved')], string='Status', required=True,
        tracking=True, copy=False, default='draft')

    def action_send_request(self):
        print("hiii")
        self.state = 'to_approve'

    def action_approve(self):
        print("hello")
        self.state = 'approved'
