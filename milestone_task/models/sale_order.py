# -*- coding: utf-8 -*-


from odoo import fields, models



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_project_button = fields.Boolean(default=False)
    task_count = fields.Integer(compute='compute_count')

    def order_tasks(self):
        """
        For creating smart button to view the corresponding tasks in sale order.
        """

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'kanban,tree',
            'res_model': 'project.task',
            'domain': [('project_id', '=', self.name)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        """
               For calculating no of tasks in this sale order.
         """
        for record in self:
            record.task_count = self.env['project.task'].search_count(
                [('project_id', '=', self.name)])


    def action_project(self):
        """
               For creating project and task from sale order
         """
        self.is_project_button = True
        project_obj = self.env['project.project']
        task_obj = self.env['project.task']

        project = project_obj.create({'name': self.name})

        for line in self.order_line:
            if line.milestone:
                task_name = f"Milestone {line.milestone}"
                parent_task = task_obj.search([('project_id', '=', project.id), ('name', '=', task_name)])
                if parent_task:
                    parent_task.write({'child_ids': [fields.Command.create({'name': line.product_id.name})]})
                else:
                    parent_task = task_obj.create({
                        'name': task_name,
                        'project_id': project.id,
                        'child_ids': [fields.Command.create({'name': line.product_id.name})]
                    })
                line.task_id = parent_task.child_ids.filtered(lambda t: t.name == line.product_id.name)
                print(line.task_id)

    def action_update_project(self):
        """
        To update created tasks.
        """
        project = self.env['project.project'].search([('name', '=', self.name)],limit=1)
        #print(project)

        for line in self.order_line:
            if line.milestone:
                task_name = f"Milestone {line.milestone}"
                child_task_name = f"Milestone {line.milestone} - {line.product_id.name}"

                parent_task = self.env['project.task'].search([('project_id', '=', project.id),
                             ('name', '=', task_name),('parent_id', '=', False)], limit=1)

                if not parent_task:
                    parent_task = self.env['project.task'].create({
                        'name': task_name,'project_id': project.id,
                    })
                if line.task_id:
                    line.task_id.write({'name': child_task_name,
                        'parent_id': parent_task.id,'project_id': project.id})
                else:
                    child_task = self.env['project.task'].create({'name': child_task_name,
                        'parent_id': parent_task.id,'project_id': project.id})
                    line.task_id = child_task


