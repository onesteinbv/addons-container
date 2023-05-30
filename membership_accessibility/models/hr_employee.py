from odoo import models


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    def get_member_groups(self):
        groups = super(HREmployee, self).get_member_groups()
        groups.append(self.env.ref('sales_team.group_sale_salesman').id)
        groups.append(self.env.ref('project.group_project_user').id)
        groups.append(self.env.ref('hr_timesheet.group_hr_timesheet_user').id)
        return groups
