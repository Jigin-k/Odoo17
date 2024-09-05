import time
import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.tools import float_is_zero
from odoo.tools import date_utils
import io
import json

from odoo.exceptions import ValidationError

try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class OrderXlsxWizard(models.TransientModel):
   _name = "order.xlsx.wizard"
   _description = "Order XLSX Report"
   subscription_ids = fields.Many2many("subscription.order",
                                       string="Subscription")
   period = fields.Selection(
       selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                  ('monthly', 'Monthly'),
                  ('yearly', 'Yearly'), ('custom', 'Custom Dates')],
       string="Period", default="daily", required=True)
   from_date = fields.Date(string="From")
   to_date = fields.Date(string="To")

   def print_xlsx(self):
       if self.from_date > self.to_date:
           raise ValidationError('Start Date must be less than End Date')
       data = {
           'subscription_ids': self.subscription_ids.ids,
           'period': self.period,
           'from_date': self.from_date,
           'to_date': self.to_date
       }
       print(data)
       return {
           'type': 'ir.actions.report',
           'data': {'model': 'order.xlsx.wizard',
                    'options': json.dumps(data,
                                          default=date_utils.json_default),
                    'output_format': 'xlsx',
                    'report_name': 'Excel Report',
                    },
           'report_type': 'xlsx',
       }
   def get_xlsx_report(self, data, response):
       print("tessstttt")
       subscriptions = data['subscription_ids']
       from_date = data['from_date']
       to_date = data['to_date']
       output = io.BytesIO()
       workbook = xlsxwriter.Workbook(output, {'in_memory': True})
       sheet = workbook.add_worksheet()
       cell_format = workbook.add_format(
           {'font_size': '12px', 'align': 'center'})
       head = workbook.add_format(
           {'align': 'center', 'bold': True, 'font_size': '20px'})
       txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
       sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
       sheet.merge_range('A6:B6', 'From Date:', cell_format)
       sheet.merge_range('C6:D6', from_date, txt)
       sheet.write('F6', 'To Date:', cell_format)
       sheet.merge_range('G6:H6', to_date, txt)
       workbook.close()
       output.seek(0)
       response.stream.write(output.read())
       output.close()
