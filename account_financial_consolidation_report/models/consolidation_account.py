# © 2011 Guewen Baconnier (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).-
from odoo import api, fields, models


class ConsolidationAccount(models.Model):
    _inherit = "consolidation.account"

    centralized = fields.Boolean(
        help="If flagged, no details will be displayed in "
        "the General Ledger report (the webkit one only), "
        "only centralized amounts per period.",
    )

    # TODO: Remove all following when André introduces them properly
    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("asset_cash", "Bank and Cash"),
            ("asset_current", "Current Assets"),
            ("asset_non_current", "Non-current Assets"),
            ("asset_prepayments", "Prepayments"),
            ("asset_fixed", "Fixed Assets"),
            ("liability_payable", "Payable"),
            ("liability_credit_card", "Credit Card"),
            ("liability_current", "Current Liabilities"),
            ("liability_non_current", "Non-current Liabilities"),
            ("equity", "Equity"),
            ("equity_unaffected", "Current Year Earnings"),
            ("income", "Income"),
            ("income_other", "Other Income"),
            ("expense", "Expenses"),
            ("expense_depreciation", "Depreciation"),
            ("expense_direct_cost", "Cost of Revenue"),
            ("off_balance", "Off-Balance Sheet"),
        ],
        string="Type",
        required=True,
    )
    internal_group = fields.Selection(
        selection=[
            ("equity", "Equity"),
            ("asset", "Asset"),
            ("liability", "Liability"),
            ("income", "Income"),
            ("expense", "Expense"),
            ("off_balance", "Off Balance"),
        ],
        readonly=True,
        compute="_compute_internal_group",
        store=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Account Currency",
        help="Forces all moves for this account to have this account currency.",
        tracking=True,
    )

    @api.depends("account_type")
    def _compute_internal_group(self):
        for account in self:
            if account.account_type:
                account.internal_group = (
                    "off_balance"
                    if account.account_type == "off_balance"
                    else account.account_type.split("_")[0]
                )
