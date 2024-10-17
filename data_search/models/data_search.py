# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DataSearch(models.Model):
    _name = 'data.search'
    _description = "Data Search"

    name = fields.Char('Search Text', required=True, search='_search_record')
    model_id = fields.Many2one('ir.model', 'Model Name')
    field_id = fields.Many2one('ir.model.fields', 'Field Name')
    records = fields.One2many('search.result', 'search_id', string='Fields',
                              required=True, copy=True)

    @api.onchange('model_id')
    def get_fields(self):
        if self.model_id:
            domain = [('model_id.id', '=', self.model_id.id)]
        else:
            domain = []
        return {'domain': {'field_id': domain}}

    def search_content(self):
        if self.name:
            self.records = [
                fields.Command.clear()]

            if self.model_id and self.field_id:
                Model = self.env[self.model_id.model]
                field_name = self.field_id.name
                results = Model.search([(field_name, 'ilike', self.name)])

                for rec in results:
                    print(rec.id)

                    self.env['search.result'].create({
                        'search_id': self.id,
                        'name': rec.name,
                        'create_date': rec.create_date,
                        'record_id': rec.id,
                        'model_name': self.model_id.model,
                        'field_name': field_name
                    })

            elif self.model_id and not self.field_id:
                Model = self.env[self.model_id.model]
                text_fields = self.env['ir.model.fields'].search(
                    [('model_id', '=', self.model_id.id), ('store', '=', True)])
                for field in text_fields:
                    results = Model.search([(field.name, 'ilike', self.name)])
                    for rec in results:
                        self.env['search.result'].create({
                            'search_id': self.id,
                            'name': rec.name,
                            'record_id': rec.id,
                            'create_date': rec.create_date,
                            'model_name': self.model_id.model,
                            'field_name': field.name
                        })


            else:
                models = self.env['ir.model'].sudo().search([])
                for model in models:
                    if model.id:
                        # print(model)
                        Model = self.env[model.model]
                        print(Model)
                        text_fields = self.env['ir.model.fields'].sudo().search(
                        [('model_id', '=', model.id)])
                        for field in text_fields:
                            print(field.name)
                        #     results = Model.sudo().search(
                        #         [])
                        #     print(results)
                        # for rec in results:
                        #     vals = {
                        #         'search_id': self.id,
                        #         'name': rec.name,
                        #         'create_date': rec.create_date
                        #     }
                        #     # if rec.id:
                        #     #     vals['record_id']= rec.id
                        #     self.env['search.result'].create(vals)
                        #     break

            return True
