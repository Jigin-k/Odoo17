from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    related_orders = fields.Many2many(comodel_name='sale.order',
                                    string='Related Sales Orders',
                                    domain ="[('partner_id','=',partner_id),('invoice_status','=','to invoice')]")

    def update_invoice_line(self):
        remove_lines = self.invoice_line_ids.filtered(
            lambda line: line.sale_line_id and line.sale_line_id.order_id not in self.related_orders)
        remove_lines.unlink()
        existing_sale_lines = self.invoice_line_ids.mapped('sale_line_id')
        print(existing_sale_lines)
        for order in self.related_orders:
            for order_line in order.order_line:
                if order_line not in existing_sale_lines:
                    self.env['account.move.line'].create({
                        'move_id': self.id,
                        'product_id': order_line.product_id.id,
                        'name': order_line.name,
                        'quantity': order_line.product_uom_qty,
                        'price_unit': order_line.price_unit,
                        'sale_line_id': order_line.id,
                    })


    def action_post(self):
        res = super(AccountMove, self).action_post()
        for orders in self.related_orders:
            orders._create_invoices()
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Sale Order Line'
    )
    #
    # @api.model
    # def unlink(self):
    #     for line in self:
    #         print("hi")
    #         sale_order_lines = line.sale_line_id
    #         if sale_order_lines:
    #             sale_order_lines.mapped('order_id')._compute_invoice_status()
    #     return super(AccountMoveLine, self).unlink()
