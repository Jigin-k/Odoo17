# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AppManagement(models.Model):
    _name = 'app.management'
    _description = 'App Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="App Name", required=True, tracking=True)
    version_id = fields.Many2one(comodel_name="app.version",string="Version", tracking=True)
    category_id = fields.Many2one('app.category', string="Category", tracking=True)
    developer_id = fields.Many2one('res.partner', string="Developer", tracking=True)
    published_date = fields.Date("Published Date")
    description = fields.Text(string="Description", tracking=True)
    pricing = fields.Selection([('free', 'Free'), ('paid', 'Paid')], string="Pricing", default="free", tracking=True)
    price = fields.Float(string="Price", help="Applicable only if the app is paid.", tracking=True)
    download_url = fields.Char(string="Download Link", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('unpublished', 'Unpublished'),
    ], string="Status", default="draft", tracking=True)
    website_published = fields.Boolean(string="Published on Website", default=False, tracking=True)

    @api.onchange('pricing')
    def _onchange_pricing(self):
        """Ensure price is reset if app is free"""
        if self.pricing == 'free':
            self.price = 0.0


class AppCategory(models.Model):
    _name = 'app.category'
    _description = 'App Category'

    name = fields.Char(string="Category Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)

class AppVersion(models.Model):
    _name = 'app.version'
    _description = 'App Version'

    name = fields.Char(string="Version Name", required=True, tracking=True)
