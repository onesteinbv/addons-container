# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.osv import expression


class ConsolidationChart(models.Model):
    _name = "consolidation.chart"
    _description = "Consolidation Chart of Accounts"
    
    name = fields.Char(required=True, index=True)
    company_ids = fields.Many2many(
        comodel_name='res.company', 
        string="Companies")
    mandatory = fields.Boolean(
        default=False, 
        help="This chart is a mandatory chart and should always be configured on a normal account.")
    consolidation_account_ids = fields.One2many(
        comodel_name="consolidation.account",
        inverse_name="chart_id",
        string="Consolidation Accounts")
    consolidation_accounts_count = fields.Integer(
        compute="_compute_consolidation_accounts_count",
        string="Consolidation Accounts")

    @api.depends("consolidation_account_ids")
    def _compute_consolidation_accounts_count(self):
        for rec in self:
            rec.consolidation_accounts_count = len(
                rec.consolidation_account_ids)
    
    def action_open_consolidation_accounts(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "consolidation_account.action_view_consolidation_account")
        action['context'] = {
            'search_default_chart_id': self.id,
            'default_chart_id': self.id,
        }
        return action