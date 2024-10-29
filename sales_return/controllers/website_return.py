from odoo import http
from odoo.http import request, route


class WebsiteReturn(http.Controller):

    @route('/sale_return', type='http', auth='public', website=True,
           methods=['POST'], csrf=False)
    def modal_submit(self, **kwargs):
        product_id = request.env['product.product'].sudo().browse(
            int(kwargs['product']))
        print(product_id)
        order = request.env['sale.order'].sudo().browse(int(kwargs['order_id']))
        print(order)
        qty = kwargs['qty']
        print(qty)
        reason = kwargs['reason']
        print(reason)
        vals = {
            'sale_order': order.id,
            'partner_id': order.partner_id.id,
            'product_id': product_id.id,
            'quantity' : qty,
            'reason' : reason
        }
        stock_picks = request.env['stock.picking'].search([('origin', '=', order.name)])
        moves = stock_picks.mapped('move_ids_without_package').with_user(1).filtered(lambda p: p.product_id == product_id)
        if moves:
            moves = moves.sorted('product_uom_qty', reverse=True)
            ret_order = request.env['sale.return'].with_user(1).create(vals)
            moves[0].picking_id.return_order = ret_order.id
        return request.redirect('/return-thank-you')
