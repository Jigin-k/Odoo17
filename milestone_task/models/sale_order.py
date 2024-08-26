from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def action_project(self):
        for record in self.order_line:
            print(record.name)

        for rec in self:
            # print(rec.name)
            tasks = [fields.Command.create({
                'name': rec.name,
                'project_id' : rec.name,
                'sale_line_id': rec.order_line.id.name

            })]


            project_vals = {
                'name':rec.name,
                'task_ids': tasks
            }
            if project_vals:
                self.env['project.project'].create(project_vals)

        # task_vals = {
        #      'project_id':
        # }
        #


















        # return    { 'type': 'ir.actions.act_window',
        #         'name': 'Projects',
        #         'view_mode': 'tree,form',
        #          'res_model': 'project.project',
        #         'domain': [('id', 'in', projects.ids)],
        #         'context': {'create': False},
        #      }

















































        # print(self.name)
        # # values = {
        # #     'name': self.name,
        # # }
        # self.env['project.project'].write({
        #     'name': self.name
        # })
        #

































    #     self.env['project.project'].create([fields.Command.create({
    #         'name': self.name
    #     })])
    # # def create_internal_project(env):
    #     #
    #     env['project.project'].search([]).write({'allow_timesheets': True})
    #
    #     admin = env.ref('base.user_admin', raise_if_not_found=False)
    #     if not admin:
    #         return
    #     project_ids = env['res.company'].search(
    #         [])._create_internal_project_task()
    #     env['account.analytic.line'].create([{
    #         'name': _("Analysis"),
    #         'user_id': admin.id,
    #         'date': fields.datetime.today(),
    #         'unit_amount': 0,
    #         'project_id': task.project_id.id,
    #         'task_id': task.id,
    #     } for task in project_ids.task_ids.filtered(
    #         lambda t: t.company_id in admin.employee_ids.company_id)])
    #
    #     _check_exists_collaborators_for_project_sharing(env)
    #

