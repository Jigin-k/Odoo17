# -*- coding: utf-8 -*-
from odoo import api,fields,models

class DataSearch(models.Model):
    _name = 'data.search'
    _description = "Data Search"


    name = fields.Char('Search Text')
    model_id = fields.Many2one('ir.model','Model Name')
    field_id = fields.Many2one('ir.model.fields','Field Name')
    records = fields.One2many('search.result', 'search_id', string='Fields', required=True, copy=True)

    @api.onchange('model_id')
    def get_fields(self):
        print("fieldss")
        if self.model_id:
            domain = [('model_id.id', '=', self.model_id.id)]
        else:
            domain = []
        return {'domain': {'field_id': domain}}

    def search_content(self):
        if self.name and self.model_id and self.field_id:
            Model = self.env[self.model_id.model]
            field_name = self.field_id.name

            results = Model.search([(field_name, 'ilike', self.name)])
            print(results)

            self.records = [fields.Command.clear()]
            for rec in results:
                print(rec[field_name])
                print(rec.id)
                self.env['search.result'].create({
                    'search_id': self.id,
                    'name': rec.name,
                    'record_id': rec.id,
                })
        return True