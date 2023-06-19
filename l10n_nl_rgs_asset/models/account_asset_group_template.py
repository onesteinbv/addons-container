# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountAssetGroupTemplate(models.Model):
    _name = "account.asset.group.template"
    _inherit = ['mail.thread']
    _description = 'Templates for Asset Groups'
    _order = "code"

    name = fields.Char(size=64, required=True, index=True)
    code = fields.Char(index=True)
    chart_template_id = fields.Many2one('account.chart.template', string='Chart Template')



    
