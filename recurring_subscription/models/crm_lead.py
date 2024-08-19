from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"


    order_id = fields.Many2one("subscription.order",string="Order ID")