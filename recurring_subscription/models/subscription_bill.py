# -*- coding: utf-8 -*-
from odoo import api, Command, fields, models


class SubscriptionBill(models.Model):
    _name = "subscription.bill"
    _description = "Subscription Bill"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Scheduled Bill")
    simulation = fields.Boolean(string="Simulation")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    customer_ids = fields.Many2many("res.partner", string="Customers", compute="_compute_customer_ids", readonly=False)
    active = fields.Boolean(string="Active", default=True)
    total_credit_amount = fields.Float(string="Total Credit Amount",
                                       compute='_compute_total_credit', store=True)
    subscription_order_ids = fields.One2many("subscription.order",
                                             inverse_name='bill_id',
                                             string="Subscription Order")
    credit_ids = fields.One2many("subscription.credit", inverse_name="bill_id",
                              string="Credits" )

    @api.depends('subscription_order_ids')
    def _compute_customer_ids(self):
        """To show the customers in the scheduled bill"""
        for rec in self.subscription_order_ids:
            self.write({
                'customer_ids': [fields.Command.create({
                    'name': rec.partner_id.name
                })]
            })

    def action_button(self):
        print("hiiiiii")


    def subscription_orders(self):
        """
        For creating smart button to view the corresponding orders in scheduled bill.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree',
            'res_model': 'subscription.order',
            'domain': [('bill_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    @api.depends('credit_ids.credit_amount')
    def _compute_total_credit(self):
        """
        To compute th total credits applied in the corresponding bills in the scheduled bill.
        """
        for rec in self:
            rec.total_credit_amount = sum(rec.credit_ids.mapped(
                'credit_amount'))


    def action_create_invoice(self):
        """
        To create Invoice for the subscription orders in the scheduled bill.
        """
        self.ensure_one()
        invoice_vals_list = []

        for order in self.subscription_order_ids.filtered(
                lambda orders: orders.state == 'confirm'):
            lines = [Command.create({
                'name': order.name,
                'product_id': order.product_id.id,
                'quantity': 1,
                'price_unit': order.recurring_price,
            })]
            print(lines)
            for credit in self.credit_ids:
                if credit.order_id.id==order.id:
                    lines.append(Command.create({
                        'name': credit.name,
                        'product_id': credit.product_id.id,
                        'quantity': 1,
                        'price_unit': -credit.credit_amount,
                        'tax_ids': False
                }))
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': order.partner_id.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': lines
            }
            invoice_vals_list.append(invoice_vals)

        if invoice_vals_list:
            invoices = self.env['account.move'].create(invoice_vals_list)
            self.active = False
            self.subscription_order_ids.filtered(
                lambda orders: orders.state == 'confirm').write({'state': 'done'})

            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoices',
                'view_mode': 'tree,form',
                 'res_model': 'account.move',
                'domain': [('id', 'in', invoices.ids)],
                'context': {'create': False},
             }

    def scheduled_action_create_invoice(self):
        """
        Scheduled action to create invoices for the expired bill schedules.
        """
        expired_bills = self.search([
            ('end_date', '<', fields.Date.today())
        ])
        for bill in expired_bills:
            bill.action_create_invoice()




