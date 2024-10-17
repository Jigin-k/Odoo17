from odoo import api,fields,models

class SearchResult(models.Model):
    _name = 'search.result'
    _description = "Data Search"

    search_id = fields.Many2one("data.search", "Search ID")
    name = fields.Char('Result')
    record_id = fields.Integer('Record ID')
    model_id = fields.Integer('Model ID')
    model_name = fields.Char('Model Name')
    field_name = fields.Char('Field Name')

    def redirect_to_model(self):
        print(self.record_id)
        return  {'type': 'ir.actions.act_window',
         'name': 'Related Record',
         'res_model': self.model_name,
         'view_mode': 'form',
         'res_id':self.record_id,
        'target': 'current'}