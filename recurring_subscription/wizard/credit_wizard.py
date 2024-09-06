# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError, RedirectWarning
from odoo.tools import date_utils
import io
import json
try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class CreditWizard(models.TransientModel):
    _name = 'credit.wizard'
    _description = 'Subscription credit Wizard'

    subscription_id = fields.Many2one("subscription.order",
                                      string="Subscription")
    state = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')])

    def action_pdf_report(self):

        data = {
            'subscription_id': self.subscription_id.id,
            'state': self.state
        }
        print(data)
        return self.env.ref(
            'recurring_subscription.action_report_subscription_credit').report_action(
            None, data=data)

    def action_xlsx_report(self):
        data = {
            'subscription_id': self.subscription_id.id,
            'state': self.state
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'credit.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = """
                          select sc.id,sc.name as credit,so.name as subscription,pr.name as customer,
                          sc.credit_amount as credit_applied,so.recurring_price - sc.credit_amount
                          as amount_pending,cr.symbol as currency ,CASE
                          WHEN sc.state = 'pending' THEN 'Pending'
                          WHEN sc.state = 'confirmed' THEN 'Confirmed'
                          WHEN sc.state = 'rejected' THEN 'Rejected'
                          END AS state from subscription_credit as sc
                          inner join subscription_order as so on so.id = sc.order_id
                          inner join res_partner as pr on pr.id = so.partner_id
                          inner join res_company as comp on comp.id = so.company_id
        				  inner join res_currency as cr on cr.id = comp.currency_id
                        """
        if data.get('subscription_id'):
            query += """ where sc.order_id = %s""" % data.get('subscription_id')
        if data.get('state') == 'pending':
            query += """ and sc.state = 'pending'"""
        if data.get('state') == 'confirmed':
            query += """ and sc.state = 'confirmed'"""
        if data.get('state') == 'rejected':
            query += """ and sc.state = 'rejected'"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        if not report:
            action = self.env.ref('recurring_subscription.credit_action')
            msg = _('No Records Found')
            raise RedirectWarning(msg, action.id, _('Go to Credits'))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('G3:L4', 'Subscription Credits Report', head)
        sheet.merge_range('D7:E7', 'Sl No:', cell_format)
        sheet.merge_range('F7:G7', 'Credit', cell_format)
        sheet.merge_range('H7:I7', 'Subscription', cell_format)
        sheet.merge_range('J7:K7', 'Customer', cell_format)
        sheet.merge_range('L7:M7', 'Credit Applied', cell_format)
        sheet.merge_range('N7:O7', 'Amount Pending', cell_format)
        sheet.merge_range('P7:Q7', 'State', cell_format)
        r = 7
        sn = 0
        for rep in report:
            r += 1
            sn += 1
            currency_credit_applied = f"{rep['currency']} {rep['credit_applied']}"
            currency_amount_pending = f"{rep['currency']} {rep['amount_pending']}"

            sheet.merge_range(f"D{r}:E{r}", sn, txt)
            sheet.merge_range(f"F{r}:G{r}", rep['credit'], txt)
            sheet.merge_range(f"H{r}:I{r}", rep['subscription'], txt)
            sheet.merge_range(f"J{r}:K{r}", rep['customer'], txt)
            sheet.merge_range(f"L{r}:M{r}", currency_credit_applied, txt)
            sheet.merge_range(f"N{r}:O{r}",currency_amount_pending, txt)
            sheet.merge_range(f"P{r}:Q{r}",rep['state'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()





