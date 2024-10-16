from odoo import api,fields,models

class SearchResult(models.Model):
    _name = 'search.result'
    _description = "Data Search"

    search_id = fields.Many2one("data.search", "Search ID")
    name = fields.Char('Result')
    record_id = fields.Integer('Record ID')