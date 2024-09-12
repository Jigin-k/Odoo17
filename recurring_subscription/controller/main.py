import json
from odoo import http
from odoo.http import content_disposition, request, Controller, route
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    """XlsxReport generating controller"""

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, **kw):
        """
        Generate an XLSX report based on the provided data and return it as a
        response.
        """
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(
                             'Subscription Order Report' + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


class SubscriptionWebsite(http.Controller):

    @http.route('/subscriptions', type='http', auth='public', website=True)
    def subscriptions(self, **kwargs):
        subscriptions = request.env['subscription.order'].sudo().search([])
        return request.render('recurring_subscription.subscriptions_template', {
            'subscriptions': subscriptions
        })

    @http.route('/subscriptions/orders', type='http', auth='public',
                website=True)
    def subscriptions_orders(self, **kwargs):
        partner = request.env['res.partner'].sudo().search([])
        product = request.env['product.product'].sudo().search([])
        bill = request.env['subscription.bill'].sudo().search([])
        return request.render('recurring_subscription.orders_template', {
            'partner': partner,
            'product': product,
            'bill': bill
        })

    @http.route('/credits', type='http', auth='public', website=True)
    def credits(self, **kwargs):
        credits = request.env['subscription.credit'].sudo().search([])
        return request.render(
            'recurring_subscription.subscriptions_credits_template', {
                'credits': credits
            })

    @http.route('/subscriptions/credits', type='http', auth='public',
                website=True)
    def subscriptions_credits(self, **kwargs):
        subscriptions = request.env['subscription.order'].sudo().search([])
        partner = request.env['res.partner'].sudo().search([])
        product = request.env['product.product'].sudo().search([])
        return request.render('recurring_subscription.credits_template', {
            'subscriptions': subscriptions,
            'partner': partner,
            'product': product
        })

    @http.route('/billing', type='http', auth='public',
                website=True)
    def billing(self, **kwargs):
        billing = request.env['subscription.bill'].sudo().search([])
        return request.render(
            'recurring_subscription.subscriptions_billing_template', {
                'billing': billing
            })

    @http.route('/subscriptions/billings', type='http', auth='public',
                website=True)
    def subscriptions_bills(self, **kwargs):
        return request.render('recurring_subscription.bills_template', {
        })

    @route('/orders/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def order_submit(self, **post):
        request.env['subscription.order'].sudo().create({
            'name': post.get('name'),
            'establishment_id': post.get('establishment_id'),
            'partner_id': post.get('partner_id'),
            'product_id': post.get('product_id'),
            'order_date': post.get('order_date'),
            'due_date': post.get('due_date'),
            'next_billing': post.get('next_billing'),
            'recurring_price': post.get('recurring_price'),
            'bill_id': post.get('bill_id'),
            'state': 'confirm'
        })
        # subscription_order = request.env['subscription.order'].sudo().search([('name','=',post.get('name'))])
        # subscription_order._onchange_new_date()
        return request.redirect('/orders-thank-you')

    @route('/bills/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def bill_submit(self, **post):
        request.env['subscription.bill'].sudo().create({
            'name': post.get('name'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date')
        })
        red_url = '/subscriptions/billings'
        return request.redirect(red_url)

    @route('/credits/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def credit_submit(self, **post):
        request.env['subscription.credit'].sudo().create({
            'name': post.get('name'),
            'order_id': post.get('subscription_id'),
            'partner_id': post.get('partner_id'),
            'product_id': post.get('product_id'),
            'start_date': post.get('start_date'),
            'credit_amount': post.get('credit_amount'),
        })

        return request.redirect('/credits')

    @http.route('/subscription/bill/<model("subscription.bill"):bill>',
                type='http', auth='public', website=True)
    def scheduled_bills(self, bill):
        subscription_orders = request.env['subscription.order'].search(
            [('bill_id', '=', bill.id)])
        print(subscription_orders)

        values = {
            'bill': bill,
            'subscriptions': subscription_orders
        }
        return request.render('recurring_subscription.scheduled_bills_template',
                              values)

    @http.route('/subscription_credits_snippet', type='json', auth='public')
    def subscription_credits(self):
        user_id = request.env.uid
        print(user_id)
        sub_credits = request.env['subscription.credit'].sudo().search_read(
            [('partner_id','=',request.env.user.partner_id.id)], ['name','order_id','credit_amount'],order="create_date DESC",limit=4)
        print(sub_credits)
        return sub_credits
