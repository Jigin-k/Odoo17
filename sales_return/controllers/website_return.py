from odoo import http
from odoo.http import content_disposition, request, route

class WebsiteReturn(http.Controller):

    @route('/sale_return', type='http', auth='public', website=True,
           methods=['POST'], csrf=False)
    def modal_submit(self, **post):
        request.env['sale.return'].sudo().create({
            'sale_order': post.get('order_id'),
            'partner_id': post.get('partner_id'),
            'product_id': post.get('product'),
            'quantity' : post.get('qty')
        })

        return request.redirect('/return-thank-you')
