# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _prepare_liquidity_account_vals(self, company, code, vals):
        account_vals = super()._prepare_liquidity_account_vals(company, code, vals)

        if company.account_fiscal_country_id.code == "NL":
            account_vals.setdefault("tag_ids", [])
            account_vals["tag_ids"].append(
                (4, self.env.ref("l10n_nl_rgs.account_tag_1003000").id)
            )

        return account_vals

    @api.model
    def _fill_missing_values(self, vals, protected_codes=False):
        chart_template = self.env.company.chart_template_id
        is_rgs = chart_template == self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        is_bank = vals.get("type") == "bank"
        is_cash = vals.get("type") == "cash"
        if not vals.get("default_account_id") and is_rgs and (is_bank or is_cash):
            account = chart_template._l10n_nl_rgs_get_create_bank_cash_account(
                vals["type"], self.env.company
            )
            if account:
                vals.update({"default_account_id": account.id})
                account.deprecated = False
            else:
                if is_bank:
                    raise ValidationError(_("Bank Account is required."))
                if is_cash:
                    raise ValidationError(_("Cash Account is required."))
        return super()._fill_missing_values(vals, protected_codes)

    @api.model_create_multi
    def create(self, vals_list):
        journals = super().create(vals_list)
        coa = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False)
        if not coa:
            return journals
        account_account_obj = self.env["account.account"]
        for journal in journals:
            if journal.company_id.chart_template_id == coa:
                all_accounts = account_account_obj.search(
                    [
                        ("company_id", "=", journal.company_id.id),
                        ("account_type", "!=", "asset_cash"),
                    ]
                )
                all_bank_accounts = all_accounts.filtered(
                    lambda a: "bank" in a.allowed_journal_ids.mapped("type")
                )
                for account in all_bank_accounts:
                    account.allowed_journal_ids |= journal
                if journal.default_account_id:
                    journal.default_account_id.allowed_journal_ids |= journal
        return journals
