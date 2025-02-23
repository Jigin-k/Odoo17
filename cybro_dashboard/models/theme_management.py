# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ThemeManagement(models.Model):
    _name = 'theme.management'
    _description = 'Theme Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables tracking in chatter

    name = fields.Char(string="Theme Name", required=True, tracking=True)
    version = fields.Char(string="Version", tracking=True)
    developer_id = fields.Many2one('res.partner', string="Developer", tracking=True)
    description = fields.Html(string="Description", tracking=True)
    preview_url = fields.Char(string="Preview Link", tracking=True)
    price = fields.Float(string="Price", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('unpublished', 'Unpublished')
    ], string="Status", default="draft", tracking=True)

