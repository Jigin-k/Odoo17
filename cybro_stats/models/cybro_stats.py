# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CybroStats(models.Model):
    _name = 'cybro.stats'
    _description = 'Cybrosys Statistics'
    _order = 'date asc'

    name = fields.Char(string='Title', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today())
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)

    # Digital Assets
    new_apps_published = fields.Integer(string='New Apps Published')
    new_blogs_published = fields.Integer(string='New Blogs Published')
    new_themes_published = fields.Integer(string='New Themes Published')
    new_functional_videos = fields.Integer(string='New Functional Videos')
    new_technical_videos = fields.Integer(string='New Technical Videos')
    new_reels = fields.Integer(string='New Reels')

    # HR Metrics
    employees_joined = fields.Integer(string='Employees Joined')
    employees_on_notice = fields.Integer(string='Employees on Notice Period')
    employees_resigned = fields.Integer(string='Employees Resigned')
    current_trainees = fields.Integer(string='Current Trainees')
    trainees_resigned = fields.Integer(string='Trainees Resigned')
    free_resources = fields.Integer(string='Free Resources (Bench)')

    # Business Metrics
    new_billings = fields.Integer(string='Number of Billing')
    new_success_packs = fields.Integer(string='New Success Packs')
    new_projects = fields.Integer(string='New Projects')
    lost_billing = fields.Integer(string='Lost Billing')

    # Social Media
    new_youtube_subscribers = fields.Integer(string='New YouTube Subscribers')
    new_insta_followers = fields.Integer(string='New Instagram Followers')

    # Educational Outreach
    campus_connect = fields.Integer(string='Campus Connect')

    # Assets
    working_laptops = fields.Integer(string='Working Laptops')

    # Financial Metrics
    profit = fields.Float(string='Profit', )
    account_balance = fields.Float(string='Account Balance')
    total_payable = fields.Float(string='Total Payable')
    total_receivables = fields.Float(string='Total Receivables')
    total_income = fields.Float(string='Total Income')
    total_expenses = fields.Float(string='Total Expenses')

    # Sales Metrics
    total_leads = fields.Integer(string='Total Leads')
    total_demos = fields.Integer(string='Total Demos/Discussions')
    total_requirements = fields.Integer(string='Total Requirements')

    # Website Metrics
    website_traffic = fields.Integer(string='Website Traffic')

    # Resource Metrics
    available_resources = fields.Integer(string='Available Resources')

    @api.depends('date')
    def _compute_display_name(self):
        for record in self:
            if record.date:
                record.display_name = record.date.strftime('%B-%Y')
            else:
                record.display_name = ''

    @api.model
    def get_tiles_data(self):
        record = self.search([],limit=1,order='date desc')
        print(record)
        youtube_subscribers_sum = record.new_youtube_subscribers
        instagram_followers_sum = record.new_insta_followers
        active_employees_sum = sum(record.employees_joined - record.employees_resigned for record in self.search([]))
        apps_published_sum = sum(record.new_apps_published for record in self.search([]))

        return {
            'youtube_subscribers': youtube_subscribers_sum,
            'instagram_followers': instagram_followers_sum,
            'active_employees': active_employees_sum,
            'apps_published': apps_published_sum
        }


    @api.model
    def get_all_field_values(self):
        """
        Retrieve all field values for a specific record, excluding system-generated fields.
        """
        fields_info = self.fields_get()
        records = self.search_read([], order='date desc', limit=1)
        if not records:
            return {}
        record_data = records[0]
        fields_to_remove = ['id', '__last_update', 'create_uid', 'create_date',
                            'write_uid', 'write_date', 'display_name']
        result = {}
        for field_name, value in record_data.items():
            if field_name not in fields_to_remove:
                field_string = fields_info[field_name]['string']
                result[field_string] = value
        return result

    @api.model
    def get_compared_field_values(self):
        """
        Retrieve field values for a record based on a specific date, excluding system-generated fields.
        """
        compared_data = self.env['cybro.stats'].search_read([],order='date desc')
        print(compared_data)
        if len(compared_data)>1:
            fields_info = self.fields_get()
            fields_to_remove = ['id', '__last_update', 'create_uid', 'create_date',
                            'write_uid', 'write_date', 'display_name']
            result = {}
            for field_name, value in compared_data[1].items():
                if field_name not in fields_to_remove:
                    field_string = fields_info[field_name]['string']
                    result[field_string] = value
            return result
        else:
            return {}

    @api.model
    def get_metrics_period_data(self, start_date=None, end_date=None, metrics_name=None):
        """
        Retrieve metric values for a given period based on the provided metric name.
        """
        print(start_date,end_date,metrics_name)
        model_fields = self.fields_get()
        metric_field_name = None
        result = {}

        for field, attrs in model_fields.items():
            if attrs.get('string') == metrics_name:
                metric_field_name = field
                break
        if not metric_field_name:
            return result

        domain = []
        if start_date:
            domain.append(('date', '>=', start_date))
        if end_date:
            domain.append(('date', '<=', end_date))
        records = self.search_read(domain, ['date', metric_field_name])
        result = {record['date'].strftime('%d/%m/%Y'): record[metric_field_name] for record in records}
        return result

    @api.model
    def get_distinct_months_years(self):
        records = self.search([], order='date asc')
        month_year_set = []
        for record in records:
            month_year_set.append(record.date.strftime('%B-%Y'))
        return month_year_set



