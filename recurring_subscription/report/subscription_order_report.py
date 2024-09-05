from odoo import models, api, _
from odoo.exceptions import RedirectWarning


class SubscriptionOrderReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_subscription_order"

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """select so.id,so.name as subscription,pr.name as customer,pt.name->>'en_US' as product,
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

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if not report:
            action = self.env.ref('recurring_subscription.subscription_action')
            msg = _('No Records Found')
            raise RedirectWarning(msg, action.id, _('Go to Orders'))
        return {
            'report': report,
            'doc_model': 'subscription.order',
        }
