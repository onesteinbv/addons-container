# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class TrialBalanceReportWizard(models.TransientModel):
    _inherit = "trial.balance.report.wizard"

    schema_type = fields.Selection(
        [('normal', 'Normal Accounts'), ('consolidation', 'Consolidation Accounts')],
        required=True,
        default='consolidation'
    )
    consolidation_chart_id = fields.Many2one('consolidation.chart')
    consolidation_account_ids = fields.Many2many(
        comodel_name="consolidation.account", string="Filter consolidation accounts"
    )
    consolidation_account_code_from = fields.Many2one(
        comodel_name="consolidation.account",
        help="Starting consolidation account in a range",
    )
    consolidation_account_code_to = fields.Many2one(
        comodel_name="consolidation.account",
        help="Ending consolidation account in a range",
    )
    unaffected_earnings_consolidation_account = fields.Many2one(
        comodel_name="consolidation.account",
        compute="_compute_unaffected_earnings_consolidation_account",
        store=True,
    )

    @api.depends("consolidation_chart_id")
    def _compute_unaffected_earnings_consolidation_account(self):
        account_type = "equity_unaffected"
        for record in self:
            record.unaffected_earnings_consolidation_account = self.env["consolidation.account"].search(
                [
                    ("chart_id", "=", record.consolidation_chart_id.id),
                    ("account_type", "=", account_type.id),
                ]
            )

    @api.onchange("consolidation_account_code_from", "consolidation_account_code_to")
    def on_change_consolidation_account_range(self):
        if (
            self.consolidation_account_code_from
            and self.consolidation_account_code_from.code.isdigit()
            and self.consolidation_account_code_to
            and self.consolidation_account_code_to.code.isdigit()
        ):
            start_range = int(self.consolidation_account_code_from.code)
            end_range = int(self.consolidation_account_code_to.code)
            self.consolidation_account_ids = self.env["consolidation.account"].search(
                [("code", ">=", start_range), ("code", "<=", end_range)]
            )
            if self.consolidation_chart_id:
                self.consolidation_account_ids = self.consolidation_account_ids.filtered(
                    lambda a: a.chart_id == self.consolidation_chart_id
                )

    @api.onchange("consolidation_chart_id", "schema_type")
    def onchange_consolidation_chart_id(self):
        if self.schema_type == 'consolidation':
            account_type = "equity_unaffected"
            count = self.env["consolidation.account"].search_count(
                [
                    ("account_type", "=", account_type.id),
                    ("chart_id", "=", self.consolidation_chart_id.id),
                ]
            )
            self.not_only_one_unaffected_earnings_account = count != 1

            res = {
                "domain": {
                    "consolidation_account_ids": [],
                }
            }
            if not self.consolidation_chart_id:
                return res
            else:
                res["domain"]["consolidation_account_ids"] += [("chart_id", "=", self.consolidation_chart_id.id)]
            return res

    @api.onchange("company_id", "schema_type")
    def onchange_company_id(self):
        if self.schema_type != 'consolidation':
            return super(TrialBalanceReportWizard, self).onchange_company_id()

    @api.onchange("receivable_accounts_only", "payable_accounts_only")
    def onchange_type_accounts_only(self):
        res = super(TrialBalanceReportWizard, self).onchange_type_accounts_only()
        if self.receivable_accounts_only or self.payable_accounts_only:
            domain = [("chart_id", "=", self.consolidation_chart_id.id)]
            if self.receivable_accounts_only and self.payable_accounts_only:
                domain += [("internal_group", "in", ("receivable", "payable"))]
            elif self.receivable_accounts_only:
                domain += [("internal_group", "=", "receivable")]
            elif self.payable_accounts_only:
                domain += [("internal_group", "=", "payable")]
            self.consolidation_account_ids = self.env["consolidation.account"].search(domain)
        else:
            self.consolidation_account_ids = None
        return res

    def _prepare_report_trial_balance(self):
        res = super(TrialBalanceReportWizard, self)._prepare_report_trial_balance()
        res.update({
            'schema_type': self.schema_type,
            'chart_id': self.consolidation_chart_id.id,
            'consolidation_account_ids': self.consolidation_account_ids.ids or [],
        })
        return res
