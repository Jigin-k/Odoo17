from odoo import api, fields , models
from ast import literal_eval



class BomCart(models.TransientModel):
    _inherit = 'res.config.settings'

    product_ids = fields.Many2many('product.product',string='Products')

    def set_values(self):
        res = super(BomCart, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'website_bom.bom_cart', self.product_ids.ids)
        return res


    @api.model
    def get_values(self):
        res = super(BomCart, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        products = with_user.get_param('website_bom.bom_cart')
        print(literal_eval(products))
        res.update(product_ids=[fields.Command.set(literal_eval(products))
                                 ] if products else False, )
        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bom_ids = fields.Many2many(
        'mrp.bom',
        string="Bills of Material",
        compute='_compute_bom_ids'
    )

    def _compute_bom_ids(self):
        for line in self:
            line.bom_ids = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)])



