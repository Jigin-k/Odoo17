# -*- coding: utf-8 -*-
from odoo import api, models, exceptions


class StockQuant(models.Model):
   _inherit = 'stock.quant'

   @api.constrains('quantity')
   def check_quantity_limit(self):
      for quant in self:
          print("hiihihihihiiihiihhihihiiiiiiiiiihih")
          max_allowed_qty = quant.product_id.max_on_hand_qty
          print(quant.quantity)
          print(max_allowed_qty)
          if quant.quantity > max_allowed_qty:
             raise exceptions.ValidationError(
               f"Warning: The on-hand quantity for {quant.product_id.name} exceeds the Maximum limit {max_allowed_qty}."
            )
