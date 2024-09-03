from odoo import models,api

class SubscriptionOrderReport(models.AbstractModel):
    _name = "report.recurring_subscription.subscription_order_report"


    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['subscription.order'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'subscription.order',
            'docs': docs,
            'data': data,
        }