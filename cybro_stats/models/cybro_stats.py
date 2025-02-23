# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api

class AppManagement(models.Model):
    _name = 'cybro.stats'
    _description = 'Cybrosys Statistics'
    _order = 'date asc'

    name = fields.Char(string='Title', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today())

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


    @api.model
    def get_all_field_values(self, active_id):
        fields_info = self.fields_get()

        record_data = self.search_read([('id', '=', active_id)])[0]

        fields_to_remove = ['id','__last_update', 'create_uid', 'create_date',
                            'write_uid', 'write_date', 'display_name']
        result = {}
        for field_name, value in record_data.items():
            if field_name not in fields_to_remove:
                field_string = fields_info[field_name]['string']
                result[field_string] = value
        return result

    @api.model
    def get_compared_field_values(self,filter_date):
        compared_data = self.env['cybro.stats'].search_read([('date','=',filter_date)])[0]
        fields_info = self.fields_get()
        fields_to_remove = ['id', '__last_update', 'create_uid', 'create_date',
                            'write_uid', 'write_date', 'display_name']
        result = {}
        for field_name, value in compared_data.items():
            if field_name not in fields_to_remove:
                field_string = fields_info[field_name]['string']
                result[field_string] = value
        return result

    @api.model
    def get_metrics_period_data(self, start_date, end_date, metrics_name):

        # Get the technical field name from the given string label
        model_fields = self.fields_get()
        metric_field_name = None
        result={}
        for field, attrs in model_fields.items():
            if attrs.get('string') == metrics_name:
                metric_field_name = field
                break

        # If no matching field is found, return an empty list
        if not metric_field_name:
            return []

        # Fetch records within the given date range
        domain = [('date', '>=', start_date), ('date', '<=', end_date)]
        records = self.search_read(domain, ['date', metric_field_name])
        print(records)
        result = {record['date'].strftime('%d/%m/%Y'): record[metric_field_name] for record in records}
        print(result)
        return result



