from odoo import models, api



class SubscriptionCreditReport(models.AbstractModel):
    _name = "report.recurring_subscription.report_subscription_credit"

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
                  select sc.id,sc.name as credit,so.name as subscription,pr.name as customer,
                  sc.credit_amount as credit_applied,so.recurring_price - sc.credit_amount
                  as amount_pending,cr.symbol as currency ,sc.state from subscription_credit as sc
                  inner join subscription_order as so on so.id = sc.order_id
                  inner join res_partner as pr on pr.id = so.partner_id
                  inner join res_company as comp on comp.id = so.company_id
				  inner join res_currency as cr on cr.id = comp.currency_id
                """
        if data.get('subscription_id'):
            query += """ where sc.order_id = %s"""%data.get('subscription_id')
        if data.get('state')=='pending':
            query += """ and sc.state = 'pending'"""
        if data.get('state')=='confirmed':
            query += """ and sc.state = 'confirmed'"""
        if data.get('state')=='rejected':
            query += """ and sc.state = 'rejected'"""


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        return {
            'report': report,
            'doc_model': 'subscription.credit',
        }
