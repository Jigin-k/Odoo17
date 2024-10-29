# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SaleReturn(models.Model):
    _name = 'sale.return'
    _inherit = ['portal.mixin']
    _rec_name = "name"
    _order = "name"
    _description = "Return Order"


    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('sale.return')

    name = fields.Char(string="Name", default=_('New'),
                       help='Name of return order')
    product_id = fields.Many2one('product.product', string="Product Variant",
                                 required=True)
    sale_order = fields.Many2one('sale.order', string="Sale Order",
                                 required=True)
    partner_id = fields.Many2one('res.partner', related='sale_order.partner_id' , string="Customer")
    user_id = fields.Many2one('res.users', string="Responsible",
                              default=lambda self: self.env.user)
    create_date = fields.Datetime(string="Create Date")
    quantity = fields.Float(string="Quantity", default=0)
    reason = fields.Text("Reason", help='Reason of the return')
    stock_picking = fields.One2many('stock.picking', 'return_order_pick',
                                    domain="[('return_order','=',False)]",
                                    string="Return Picking",
                                    help="Shows the return picking of the corresponding return order")
    source_pick = fields.One2many('stock.picking', 'return_order',
                                  string="Source Delivery",
                                  help="Shows the delivery orders of the corresponding return order")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'),
         ('cancel', 'Canceled')],
        string='Status', readonly=True, default='draft',)

    @api.model_create_multi
    def create(self, vals_list):
        """
        To create new sequence for order id
        """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.return') or _('New')
        return super(SaleReturn, self).create(vals_list)

    def return_confirm(self):
        if not self.source_pick:
            stock_picks = self.env['stock.picking'].search(
                [('origin', '=', self.sale_order.name)])
            moves = stock_picks.mapped('move_ids_without_package').filtered(
                lambda p: p.product_id == self.product_id)
        else:
            moves = self.source_pick.mapped(
                'move_ids_without_package').filtered(
                lambda p: p.product_id == self.product_id)
        if moves:
            moves = moves.sorted('product_uom_qty', reverse=True)
            pick = moves[0].picking_id
            vals = {'picking_id': pick.id}
            return_pick_wizard = self.env['stock.return.picking'].create(vals)
            print(return_pick_wizard)
            # return_pick_wizard._compute_moves_locations()
            # return_pick_wizard.product_return_moves.unlink()
            lines = {'product_id': self.product_id.id,
                     "quantity": self.quantity,
                     'wizard_id': return_pick_wizard.id,
                     'move_id': moves[0].id}
            self.env['stock.return.picking.line'].create(lines)
            return_pick = return_pick_wizard.action_create_returns()
            self.write({'state': 'confirm'})
