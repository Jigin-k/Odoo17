from datetime import timedelta
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from datetime import timedelta


class HREmployee(models.Model):
    _inherit = "hr.employee"

    state = fields.Selection([
        ('trainee', 'Trainee'),
        ('employee', 'Employee'),
        ('notice', 'Notice Period'),
        ('resigned', 'Resigned'),
    ], string="Employee Status", default="trainee", tracking=True)

    # Date Fields
    trainee_join_date = fields.Date(
        default=fields.Date.today(),
        string='Join Date',
        tracking=True

    )
    conversion_date = fields.Date(
        string='Join Date',
        tracking=True
    )

    notice_period_start_date = fields.Date(
        string='Notice Period Start Date',
        tracking=True
    )
    notice_period_end_date = fields.Date(
        string='Notice Period End Date',
        tracking=True
    )

    # @api.onchange('resignation_date', 'notice_period_days')
    # def _onchange_resignation_date(self):
    #     """
    #     Update notice period dates based on resignation date and notice period.
    #     """
    #     if self.resignation_date:
    #         self.notice_period_start_date = self.resignation_date
    #         self.notice_period_end_date = self.resignation_date + timedelta(days=self.notice_period_days)

    def action_convert_to_employee(self):
        """
        Change employee type to 'employee' and set conversion date to today.
        """
        self.ensure_one()
        self.write({
            'state': 'employee',
            'conversion_date': fields.Date.today()
        })
        return True

    #
    # def get_employee_counts(self):
    #     """
    #     Get key employee metrics for the dashboard.
    #     Returns counts of joined employees, employees on notice period,
    #     resigned employees, current trainees, resigned trainees,
    #     and total current employees.
    #     """
    #     today = fields.Date.today()
    #
    #     current_employees = self.env['hr.employee'].search_count([
    #         ('state', '=', 'employee'),
    #         ('active', '=', True),
    #         '|', ('resignation_date', '=', False), ('resignation_date', '>', today)
    #     ])
    #
    #     employees_on_notice = self.env['hr.employee'].search_count([
    #         ('notice_period_start_date', '<=', today),
    #         ('notice_period_end_date', '>=', today),
    #          ('resignation_date', '>', today)
    #     ])
    #
    #     employees_resigned = self.env['hr.employee'].search_count([
    #         ('notice_period_end_date', '<', today)
    #     ])
    #
    #     current_trainees = self.env['hr.employee'].search_count([
    #         ('state', '=', 'trainee'),
    #         ('active', '=', True),
    #         '|', ('resignation_date', '=', False), ('resignation_date', '>', today)
    #     ])
    #
    #     trainees_resigned = self.env['hr.employee'].search_count([
    #         ('state', '=', 'trainee'),
    #         ('resignation_date', '!=', False),
    #         ('resignation_date', '<', today)
    #     ])
    #
    #     return {
    #         'current_employees': current_employees,
    #         'employees_on_notice': employees_on_notice,
    #         'employees_resigned': employees_resigned,
    #         'current_trainees': current_trainees,
    #         'trainees_resigned': trainees_resigned,
    #     }


class HREmployeeDeparture(models.TransientModel):
    _inherit = "hr.departure.wizard"

    resignation_date = fields.Date(
        string='Resignation Date',
        required=True
    )
    notice_period_days = fields.Integer(
        string='Notice Period (Days)',
        default=90
    )
    departure_date = fields.Date(string="Departure Date", required=True,
        default=False,
        compute='_compute_departure_date')

    @api.depends('resignation_date')
    def _compute_departure_date(self):
        departure_date = self.resignation_date + timedelta(days=self.notice_period_days)
        self.departure_date = departure_date

    # def action_register_departure(self):
