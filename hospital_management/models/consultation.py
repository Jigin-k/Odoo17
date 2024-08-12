from odoo import models,fields, api
from datetime import date


class Consultation(models.Model):
    _name = "consultation.form1"
    _description = "Consultation Form"

    op_number = fields.Many2one("op.ticket",string="OP NO.")
    token_number = fields.Integer(string='Token No.')
    date = fields.Date(string="Date", default=date.today())
    patient_id = fields.Many2one("res.partner", string='Patient Name', related="op_number.patient_id")
    doctor_id = fields.Many2one("hr.employee", string='Doctor', related="op_number.doctor_id")
    department_id = fields.Many2one("hr.department", string="Department", related='doctor_id.department_id')

    @api.onchange('op_number')
    def _onchange_op_number(self):
        print(self)
        if self.op_number:
            self.token_number= self.op_number.token_number
            self.date= self.op_number.date
            self.patient_id = self.op_number.patient_id
            self.doctor_id = self.op_number.doctor_id
            self.department_id = self.op_number.department_id
