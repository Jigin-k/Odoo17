from odoo import fields, models, api, _
from datetime import date


class OpTicket(models.Model):
    _name = "op.ticket"
    _description = "OP Ticket"

    op_number = fields.Char(string='Order Reference', required=True,readonly=True, default=lambda self: _('New'))
    token_number = fields.Integer("Token Number")
    date = fields.Date(string="Date",default=date.today())
    age = fields.Integer(related='patient_id.age', string='Age')
    dob = fields.Date(related='patient_id.dob', string="Date Of Birth")
    blood_group = fields.Selection(selection=[('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'),
                                              ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'),
                                              ('o+', 'O+'), ('o-', 'O+')], string='Blood Group', related='patient_id.blood_group')
    patient_id = fields.Many2one("res.partner", string='Patient Name')
    doctor_id = fields.Many2one("hr.employee", string='Consulting Doctor')
    department_id = fields.Many2one("hr.department", string="Department", related='doctor_id.department_id')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('op_number', _('New')) == _('New'):
            vals['op_number'] = self.env['ir.sequence'].next_by_code(
                'op.ticket') or _('New')
        res = super(OpTicket, self).create(vals)
        return res

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        print(self)
        if self.patient_id:
            self.age = self.patient_id.age
            self.dob = self.patient_id.dob
            self.blood_group = self.patient_id.blood_group

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            self.department_id = self.doctor_id.department_id

    def button_to_done(self):
        self.write({'state': "done"})
