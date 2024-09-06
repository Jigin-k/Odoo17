# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import ValidationError, RedirectWarning
from odoo.tools import date_utils
import io
import json
try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


class OrderWizard(models.TransientModel):
    _name = 'order.wizard'
    _description = 'Subscription Order Wizard'

    subscription_ids = fields.Many2many("subscription.order",
                                        string="Subscription")
    period = fields.Selection(
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                   ('monthly', 'Monthly'),
                   ('yearly', 'Yearly'), ('custom', 'Custom Dates')],
        string="Period", default="daily", required=True)
    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")

    def action_print_pdf(self):
        if self.to_date and self.from_date:
            if self.from_date > self.to_date:
                raise ValidationError('From Date must be less than To Date')
        data = {
            'subscription_ids': self.subscription_ids.ids,
            'period': self.period,
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        print(data)
        return self.env.ref(
            'recurring_subscription.action_report_subscription_order').report_action(
            None, data=data)

    def action_print_xlsx(self):
        if self.to_date and self.from_date:
            if self.from_date > self.to_date:
                raise ValidationError('From Date must be less than To Date')

        data = {
            'subscription_ids': self.subscription_ids.ids,
            'period': self.period,
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        print(data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'order.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):

        # states_dict = dict(states)
        # print(states_dict)
        query = """     select so.id,so.name as subscription,pr.name as customer,pt.name->>'en_US' as product,
                        so.recurring_price as amount,so.order_date,cr.symbol as currency ,
                        so.due_date,so.next_billing,so.state from subscription_order as so
                        inner join res_partner as pr on pr.id = so.partner_id
        				inner join product_product as pp on pp.id = so.product_id
        				inner join product_template as pt on pt.id = pp.product_tmpl_id
        				inner join res_company as comp on comp.id = so.company_id
        				inner join res_currency as cr on cr.id = comp.currency_id"""

        if data.get('subscription_ids'):
            query += """ where so.id in %s""" % str(
                tuple(data.get('subscription_ids'))).replace(",)", ")")
        if data.get('period') == 'daily':
            query += """ and so.order_date = CURRENT_DATE"""
        if data.get('period') == 'weekly':
            query += """ and EXTRACT('WEEK' FROM so.order_date) = EXTRACT('WEEK' FROM CURRENT_DATE)"""
        if data.get('period') == 'monthly':
            query += """ and EXTRACT('MONTH' FROM so.order_date) = EXTRACT('MONTH' FROM CURRENT_DATE)"""
        if data.get('period') == 'yearly':
            query += """ and EXTRACT('YEAR' FROM so.order_date) = EXTRACT('YEAR' FROM CURRENT_DATE)"""
        if data.get('from_date') and not data.get('to_date'):
            query += """ and so.order_date >= '%s'""" % data.get('from_date')
        if data.get('to_date') and not data.get('from_date'):
            query += """ and so.order_date <= '%s'""" % data.get('to_date')
        if data.get('from_date') and data.get('to_date'):
            query += """ and so.order_date >= '%s' and so.order_date <= '%s'""" % (
            data.get('from_date'), data.get('to_date'))

        print(query)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        if not report:
            action = self.env.ref('recurring_subscription.subscription_action')
            msg = _('No Records Found')
            raise RedirectWarning(msg, action.id, _('Go to Orders'))


        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'bold': True})
        cell_format2 = workbook.add_format(
            {'font_size': '10px', 'align': 'right', 'bold': True})
        cell_format3 = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})

        states = self.env['subscription.order']._fields['state'].selection
        states_dict = dict(states)

        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('G3:L4', 'Subscription Orders Report', head)
        sheet.merge_range('D7:E7', 'Sl No:', cell_format)
        sheet.merge_range('F7:G7', 'Subscription', cell_format)
        sheet.merge_range('H7:I7', 'Customer', cell_format)
        sheet.merge_range('J7:K7', 'Product', cell_format)
        sheet.merge_range('L7:M7', 'Amount', cell_format)
        sheet.merge_range('N7:O7', 'State', cell_format)
        r = 7
        sn = 0
        total = 0
        for rep in report:
            r += 1
            sn += 1
            total += rep['amount']
            currency_amount = f"{rep['currency']} {rep['amount']}"

            sheet.merge_range(f"D{r}:E{r}", sn, txt)
            sheet.merge_range(f"F{r}:G{r}", rep['subscription'], txt)
            sheet.merge_range(f"H{r}:I{r}", rep['customer'], txt)
            sheet.merge_range(f"J{r}:K{r}", rep['product'], txt)
            sheet.merge_range(f"L{r}:M{r}", currency_amount,txt)
            sheet.merge_range(f"N{r}:O{r}", states_dict[rep['state']], txt)
        sheet.merge_range(f"D{r + 1}:K{r + 1}", "Subtotal :", cell_format2)
        sheet.merge_range(f"L{r + 1}:M{r+1}", f"{report[0]['currency']} {total}",
                          cell_format3)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
