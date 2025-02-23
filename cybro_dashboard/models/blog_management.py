# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BlogManagement(models.Model):
    _name = 'blog.management'
    _description = 'Blog Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables tracking in chatter

    name = fields.Char(string="Title", required=True, tracking=True)
    author_id = fields.Many2one('res.partner', string="Author", tracking=True)
    category_id = fields.Many2one('blog.category', string="Category", tracking=True)
    content = fields.Html(string="Content", tracking=True)
    published_date = fields.Date(string="Published Date", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string="Status", default="draft", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure state is updated when website_published is enabled at creation."""
        for vals in vals_list:
            if vals.get("website_published"):
                vals["state"] = "published"
        return super().create(vals_list)

class BlogCategory(models.Model):
    _name = 'blog.category'
    _description = 'Blog Category'

    name = fields.Char(string="Category Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
