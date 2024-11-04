# -*- coding: utf-8 -*-
from odoo import models, fields

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    avg_landed_cost_lines = fields.One2many(
        'stock.avg.landed.cost.line', 'landed_cost_id',
        'Averege Landed Cost', )


    def compute_avg_landed_cost(self):
        self.avg_landed_cost_lines.unlink()
        avg_line_vals = []
        for rec in self.valuation_adjustment_lines:
             avg_line_vals.append({
                'landed_cost_id': self.id,
                'product_id': rec.product_id.id,
                'avg_landed_cost': rec.additional_landed_cost/rec.quantity,
            })
        print(avg_line_vals)
        for vals in avg_line_vals:
            self.env['stock.avg.landed.cost.line'].create(vals)
        return True


class StockAvgLandedCostLine(models.Model):
    _name = 'stock.avg.landed.cost.line'
    _description = 'Average Landed Cost Line'

    landed_cost_id = fields.Many2one(
        'stock.landed.cost',
        string='Landed Cost',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    avg_landed_cost = fields.Float(
        string='Avg Landed Cost',
    )



