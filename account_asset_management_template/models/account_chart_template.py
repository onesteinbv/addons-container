# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load_template(
        self, company, code_digits=None, account_ref=None, taxes_ref=None
    ):
        self.ensure_one()
        if not code_digits:
            code_digits = self.code_digits

        account_ref, taxes_ref = super(AccountChartTemplate, self)._load_template(
            company,
            code_digits=code_digits,
            account_ref=account_ref,
            taxes_ref=taxes_ref,
        )

        # Generate Asset Groups from Templates
        asset_group_ref = self.generate_account_asset_groups(company)

        # Generate Asset Profiles from Templates
        self.generate_account_asset_profile(asset_group_ref, company)

        return account_ref, taxes_ref

    def generate_account_asset_groups(self, company):
        self.ensure_one()
        asset_group_ref = {}
        group_templates = self.env["account.asset.group.template"].search(
            [("chart_template_id", "=", self.id)]
        )
        template_vals = []
        for group_template in group_templates:
            vals = {
                "name": group_template.name,
                "code": group_template.code,
                "company_id": company.id,
            }
            template_vals.append((group_template, vals))
        groups = self._create_records_with_xmlid(
            "account.asset.group", template_vals, company
        )

        for template, group in zip(group_templates, groups):
            asset_group_ref[template] = group
        return asset_group_ref

    def generate_account_asset_profile(self, asset_group_ref, company):
        self.ensure_one()

        def _get_account_id(template, company):
            [external_id] = template.get_external_id().values()
            (name, module) = external_id.split(".")
            external_name = "%s.%d_%s" % (name, company.id, module)
            _, res_id = self.env["ir.model.data"]._xmlid_to_res_model_res_id(
                external_name
            )
            return res_id

        profiles = self.env["account.asset.profile.template"].search(
            [("chart_template_id", "=", self.id)]
        )

        # create asset profiles
        template_vals = []
        for profile in profiles:
            account_asset_id = _get_account_id(profile.account_asset_id, company)
            vals = {
                "name": profile.name,
                "account_asset_id": account_asset_id,
                "account_expense_depreciation_id": _get_account_id(
                    profile.account_expense_depreciation_id, company
                ),
                "account_depreciation_id": _get_account_id(
                    profile.account_depreciation_id, company
                ),
                "group_ids": [asset_group_ref[group].id for group in profile.group_ids],
                "days_calc": profile.days_calc,
                "asset_product_item": profile.asset_product_item,
                "method_number": profile.method_number,
                "method_period": profile.method_period,
                "method_time": profile.method_time,
                "method_progress_factor": profile.method_progress_factor,
                "note": profile.note,
                "company_id": company.id,
                "prorata": profile.prorata,
            }
            if profile.journal_code:
                journal = self.env["account.journal"].search(
                    [
                        ("code", "=", profile.journal_code),
                        ("company_id", "=", company.id),
                    ]
                )
                if journal:
                    vals["journal_id"] = journal.id
            if account_asset_id:
                template_vals.append((profile, vals))
        self._create_records_with_xmlid("account.asset.profile", template_vals, company)
