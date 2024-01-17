# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAssetProfileTemplate(models.Model):
    _name = "account.asset.profile.template"
    _inherit = ["mail.thread"]
    _description = "Templates for Asset Profiles"
    _order = "name"

    name = fields.Char(required=True)
    note = fields.Text()
    account_asset_id = fields.Many2one(
        string="Asset Account", comodel_name="account.account.template"
    )
    account_depreciation_id = fields.Many2one(
        string="Depreciation Account", comodel_name="account.account.template"
    )
    account_expense_depreciation_id = fields.Many2one(
        string="Depr. Expense Account", comodel_name="account.account.template"
    )
    journal_code = fields.Char()
    group_ids = fields.Many2many(
        comodel_name="account.asset.group.template",
        relation="account_asset_profile_template_group_rel",
        column1="profile_id",
        column2="group_id",
        string="Asset Template Groups",
    )
    method = fields.Selection(
        selection=lambda self: self._selection_method(),
        string="Computation Method",
        default="linear",
    )
    method_number = fields.Integer(
        string="Number of Years",
        help="The number of years needed to depreciate your asset",
        default=5,
    )
    method_period = fields.Selection(
        selection=lambda self: self._selection_method_period(),
        string="Period Length",
        default="year",
    )
    method_progress_factor = fields.Float(string="Degressive Factor", default=0.3)
    method_time = fields.Selection(
        selection=lambda self: self._selection_method_time(),
        string="Time Method",
        default="year",
    )
    days_calc = fields.Boolean(string="Calculate by days", default=False)
    prorata = fields.Boolean(string="Prorata Temporis")
    asset_product_item = fields.Boolean(string="Create an asset by product item")
    chart_template_id = fields.Many2one("account.chart.template")

    @api.model
    def _selection_method(self):
        return self.env["account.asset.profile"]._selection_method()

    @api.model
    def _selection_method_period(self):
        return self.env["account.asset.profile"]._selection_method_period()

    @api.model
    def _selection_method_time(self):
        return self.env["account.asset.profile"]._selection_method_time()
