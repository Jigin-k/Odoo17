from odoo import models,api

class SubscriptionOrderReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_subscription_order"


    @api.model
    def _get_report_values(self, docids, data=None):
        print("hi")
        docs = self.env['subscription.order'].search([])
        print(docs)
        query = """select so.id,so.name as subscription,pr.name as customer,pt.name->>'en_US' as product,
so.recurring_price as amount,so.order_date,
so.due_date,so.next_billing,so.state from subscription_order as so
                inner join res_partner as pr on pr.id = so.partner_id
				inner join product_product as pp on pp.id = so.product_id
				inner join product_template as pt on pt.id = pp.product_tmpl_id"""


        if data.get('subscription_ids'):
            query += """ where so.id in '%s'""" % (str(tuple(data.get('subscription_ids'))))
        if data.get('period') == 'daily':
            query += """ and so.order_date = CURRENT_DATE"""
        if data.get('period') == 'weekly':
            query += """ and EXTRACT('WEEK' FROM so.order_date) = EXTRACT('WEEK' FROM CURRENT_DATE)"""
        if data.get('period') == 'monthly':
            query += """ and EXTRACT('MONTH' FROM so.order_date) = EXTRACT('MONTH' FROM CURRENT_DATE)"""
        if data.get('period') == 'yearly':
            query += """ and EXTRACT('YEAR' FROM so.order_date) = EXTRACT('YEAR' FROM CURRENT_DATE)"""

        print(query)
        self.env.cr.execute(query.replace("'(", "(").replace(")'", ")").replace(",)", ")"))
        report = self.env.cr.dictfetchall()
        return {
             'report':report,
            'doc_model': 'subscription.order',
        }



