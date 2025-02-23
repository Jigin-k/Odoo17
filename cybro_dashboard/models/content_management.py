from odoo import models, fields, api

class ContentManagement(models.Model):
    _name = 'training.video'
    _description =  'Training Videos'
    _order = 'create_date desc'

    name = fields.Char(string='Title', required=True)
    video_type = fields.Selection([
        ('functional', 'Functional'),
        ('technical', 'Technical')
    ], string='Video Type', required=True)
    description = fields.Text(string='Description')
    upload_date = fields.Date(string='Upload Date', default=fields.Date.today)
    # duration = fields.Float(string='Duration (minutes)')
    url = fields.Char(string='Video URL')
    # views = fields.Integer(string='View Count', default=0)
    # category = fields.Selection([
    #     ('beginner', 'Beginner'),
    #     ('intermediate', 'Intermediate'),
    #     ('advanced', 'Advanced')
    # ], string='Category', default='beginner')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft')

    @api.model
    def get_video_stats(self):
        total_videos = self.search_count([])
        published_videos = self.search_count([('state', '=', 'published')])
        total_views = sum(self.search([]).mapped('views'))
        return {
            'total_videos': total_videos,
            'published_videos': published_videos,
            'total_views': total_views,
        }

class Reel(models.Model):
    _name = 'social.reel'
    _description = 'Social Media Reels'
    _order = 'create_date desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    upload_date = fields.Date(string='Upload Date', default=fields.Date.today)
    # platform = fields.Selection([
    #     ('instagram', 'Instagram'),
    #     ('youtube', 'YouTube Shorts'),
    #     ('tiktok', 'TikTok')
    # ], string='Platform', required=True)
    # duration = fields.Float(string='Duration (seconds)')
    url = fields.Char(string='Reel URL')
    # views = fields.Integer(string='View Count', default=0)
    # likes = fields.Integer(string='Like Count', default=0)
    # shares = fields.Integer(string='Share Count', default=0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft')

    @api.model
    def get_reel_stats(self):
        total_reels = self.search_count([])
        platform_counts = {
            'instagram': self.search_count([('platform', '=', 'instagram')]),
            'youtube': self.search_count([('platform', '=', 'youtube')]),
            'tiktok': self.search_count([('platform', '=', 'tiktok')])
        }
        total_views = sum(self.search([]).mapped('views'))
        total_likes = sum(self.search([]).mapped('likes'))
        return {
            'total_reels': total_reels,
            'platform_counts': platform_counts,
            'total_views': total_views,
            'total_likes': total_likes,
        }