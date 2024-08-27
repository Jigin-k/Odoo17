from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_project(self):
        print(self.id)
        project_name = f"Project {self.name}"
        project = self.env['project.project'].create({
            'name': project_name,
        })

        milestone_tasks = {}

        for rec in self.order_line:
            if rec.milestone:
                if rec.milestone not in milestone_tasks:
                    parent_task = self.env['project.task'].create({
                        'name': f"Milestone {rec.milestone}",
                        'project_id': project.id,
                    })
                    milestone_tasks[rec.milestone] = parent_task
                    print(f"Created parent task: {parent_task.name}")

                child_task = self.env['project.task'].create({
                    "name": f"Milestone {rec.milestone} - {rec.product_id.name}",
                    "parent_id": milestone_tasks[rec.milestone].id,
                    "project_id": project.id,
                })

    def action_update_project(self):
        print('haaaaiii')
