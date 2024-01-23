# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import Command, _, api, models


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):

        if self != self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False):
            return super(AccountChartTemplate, self)._prepare_all_journals(
                acc_template_ref, company, journals_dict=journals_dict
            )

        journals_dict = [
            {
                "name": _("Accruals"),
                "type": "general",
                "code": _("ACCR"),
                "favorite": True,
                "color": 11,
                "sequence": 15,
            },
            {
                "name": _("Depreciations"),
                "type": "general",
                "code": "DEPR",
                "favorite": True,
                "color": 11,
                "sequence": 16,
            },
            {
                "name": _("Foreign currency revaluation"),
                "type": "general",
                "code": _("FCR"),
                "favorite": True,
                "sequence": 17,
            },
            {
                "name": _("Wages"),
                "type": "general",
                "code": _("WAG"),
                "favorite": True,
                "sequence": 18,
            },
            {
                "name": _("Inventory Valuation"),
                "type": "general",
                "code": _("STJ"),
                "favorite": True,
                "sequence": 19,
            },
        ]
        resp_journals = super(AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict=journals_dict
        )

        # Archive unwanted journals
        for journal in resp_journals:
            if journal["code"] == "CABA":
                journal["active"] = False

        return resp_journals

    @api.model
    def _prepare_transfer_account_for_direct_creation(self, name, company):
        res = super(
            AccountChartTemplate, self
        )._prepare_transfer_account_for_direct_creation(name, company)
        if company.account_fiscal_country_id.code == "NL":
            xml_id = self.env.ref("l10n_nl_rgs.account_tag_1003000").id
            res.setdefault("tag_ids", [])
            res["tag_ids"].append((4, xml_id))
        return res

    @api.model
    def _create_liquidity_journal_suspense_account(self, company, code_digits):
        account = super()._create_liquidity_journal_suspense_account(
            company, code_digits
        )
        if company.account_fiscal_country_id.code == "NL":
            account.tag_ids = [
                Command.link(self.env.ref("l10n_nl_rgs.account_tag_1003000").id)
            ]
            if account.referentiecode:
                account.reconcile = True

                installed_langs = dict(self.env["res.lang"].get_installed())
                # Install Dutch language if not done yet
                lang = "nl_NL"
                if lang not in installed_langs:
                    self.env["res.lang"]._activate_lang(lang)
                account.update_field_translations(
                    "name", {"nl_NL": "Nog af te letteren bank"}
                )
        return account

    def _get_account_vals(self, company, account_template, code_acc, tax_template_ref):
        self.ensure_one()
        vals = super()._get_account_vals(
            company, account_template, code_acc, tax_template_ref
        )

        if self == self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False):
            vals.update(
                {
                    "referentiecode": account_template.referentiecode,
                    "sort_code": account_template.sort_code,
                }
            )
        return vals

    def generate_account(
        self, tax_template_ref, acc_template_ref, code_digits, company
    ):
        if self != self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False):
            return super().generate_account(
                tax_template_ref, acc_template_ref, code_digits, company
            )

        self.ensure_one()
        account_tmpl_obj = self.env["account.account.template"]
        acc_template = account_tmpl_obj.search(
            [("chart_template_id", "=", self.id)], order="id"
        )
        template_vals = []
        acc_template_done = self.env["account.account.template"]
        for account_template in acc_template:
            acc_template_done |= account_template
            code_main = account_template.code and len(account_template.code) or 0
            code_acc = account_template.code or ""
            if code_main > 0 and code_main <= code_digits:
                code_acc = str(code_acc) + (str("0" * (code_digits - code_main)))
            vals = self._get_account_vals(
                company, account_template, code_acc, tax_template_ref
            )
            if account_template.nocreate:
                vals.update(
                    {
                        "deprecated": True,
                    }
                )
            template_vals.append((account_template, vals))
        accounts = self._create_records_with_xmlid(
            "account.account", template_vals, company
        )
        for template, account in zip(acc_template_done, accounts):
            acc_template_ref[template] = account
        return acc_template_ref

    def generate_account_groups(self, company):
        """Inherit this method to fix reference code missing in account groups"""
        self.ensure_one()

        if self != self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False):
            return super().generate_account_groups(company)

        # Overrides standard Odoo method
        group_templates = self.env["account.group.template"].search(
            [("chart_template_id", "=", self.id)]
        )
        template_vals = []
        for group_template in group_templates:
            vals = {
                "name": group_template.name,
                "code_prefix_start": group_template.code_prefix_start,
                "code_prefix_end": group_template.code_prefix_end,
                "company_id": company.id,
                "code": group_template.code,
                "referentiecode": group_template.referentiecode,
                "sort_code": group_template.sort_code,
            }
            template_vals.append((group_template, vals))

        groups = self._create_records_with_xmlid(
            "account.group", template_vals, company
        )

        for group_template in group_templates.filtered(lambda agt: agt.parent_id):
            parent_group = groups.filtered(
                lambda ag: ag.code == group_template.parent_id.code
            )
            group = groups.filtered(lambda ag: ag.code == group_template.code)
            if group and parent_group:
                group.parent_id = parent_group.id

    def _load(self, company):
        res = super()._load(company)
        rgs = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        if rgs and self == rgs:

            # Add allowed journals to accounts based on group settings
            if not company.l10n_nl_rgs_disable_allowed_journals:
                self.add_account_allowed_journals(company)

            # Workaround to translate journal names to Dutch
            self._translate_journal_names_to_dutch(company)

            # Set liquidity transfer template: 1003010 (delete 1003011)
            self._set_liquidity_transfer_account_template()

            # Set the transfer account 1003010 on the company (delete 1003011)
            self._set_liquidity_transfer_account(company)

        return res

    def _set_liquidity_transfer_account(self, company):
        """Set the transfer account 1003010 on the company (delete 1003011)"""
        # set account 1003010
        transfer_account = self.env["account.account"].search(
            [("code", "=", "1003010"), ("company_id", "=", company.id)], limit=1
        )
        if transfer_account and company.transfer_account_id != transfer_account:
            company.transfer_account_id = transfer_account

        # delete account 1003011
        wrong_transfer_account = self.env["account.account"].search(
            [("code", "=", "1003011"), ("company_id", "=", company.id)], limit=1
        )
        if (
            wrong_transfer_account
            and company.transfer_account_id != wrong_transfer_account
        ):
            wrong_transfer_account.unlink()

    def _set_liquidity_transfer_account_template(self):
        """Set liquidity transfer template: 1003010 (delete 1003011)"""
        rgs = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        rgs_xml_id = "l10n_nl_rgs.l10nnl_rgs_chart_template_liquidity_transfer"
        liquidity_account_template = self.env.ref(rgs_xml_id, raise_if_not_found=False)
        if liquidity_account_template and liquidity_account_template.code == "1003011":
            # liquidity transfer account template
            correct_account_template = self.env["account.account.template"].search(
                [
                    ("code", "=", "1003010"),
                    ("chart_template_id", "=", rgs.id),
                ]
            )
            if len(correct_account_template) == 1:
                account_data = dict(
                    xml_id=rgs_xml_id,
                    record=correct_account_template,
                    noupdate=True,
                )
                self.env["ir.model.data"]._update_xmlids([account_data])
                liquidity_account_template.unlink()

    def add_account_allowed_journals(self, company):
        """Inherit this method to fix reference code missing in account groups"""
        self.ensure_one()

        group_templates = self.env["account.group.template"].search(
            [
                ("chart_template_id", "=", self.id),
                "|",
                ("rgs_allowed_journals_code", "!=", False),
                ("rgs_allowed_journals_type", "!=", False),
            ]
        )
        referentiecodes = group_templates.mapped("referentiecode")
        all_groups = self.env["account.group"].search(
            [("company_id", "=", company.id), ("referentiecode", "in", referentiecodes)]
        )
        all_journals = self.env["account.journal"].search(
            [
                ("company_id", "=", company.id),
            ]
        )
        accrual_journal = all_journals.filtered(lambda j: j.code == "ACCR")

        for group_template in group_templates:
            group = all_groups.filtered(
                lambda g: g.referentiecode == group_template.referentiecode
            )
            if not group:
                continue
            journals = self.env["account.journal"]
            if group_template.rgs_allowed_journals_type:
                type_list = [
                    jtype
                    for jtype in group_template.rgs_allowed_journals_type.split(",")
                ]
                journals |= self.get_allowed_account_journals_based_on_type(
                    all_journals, type_list
                )
            if group_template.rgs_allowed_journals_code:
                code_list = [
                    jcode
                    for jcode in group_template.rgs_allowed_journals_code.split(",")
                ]
                journals |= self.get_allowed_account_journals_based_on_code(
                    all_journals, code_list
                )

            if journals:
                accounts = group.get_all_account_ids()
                for account in accounts:
                    account.allowed_journal_ids |= journals
                    if accrual_journal and account.account_type == "asset_prepayments":
                        account.allowed_journal_ids |= accrual_journal

    def get_allowed_account_journals_based_on_type(self, all_journals, type_list):
        return all_journals.filtered(lambda j: j.type in type_list)

    def get_allowed_account_journals_based_on_code(self, all_journals, code_list):
        # Not so nice fix, needs more testing and different approach
        nl_mapping = {"MISC": "MEM", "WAG": "SAL", "DEPR": "AFSC"}
        for k, v in nl_mapping.items():
            if k in code_list and v not in code_list:
                code_list.append(v)
        return all_journals.filtered(lambda j: j.code in code_list)

    def _create_bank_journals(self, company, acc_template_ref):
        self.ensure_one()
        if self != self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False):
            return super()._create_bank_journals(company, acc_template_ref)

        bank_journals = self.env["account.journal"]
        # Create the journals that will trigger the account.account creation
        for acc in self._get_default_bank_journals_data():
            vals = {
                "name": acc["acc_name"],
                "type": acc["account_type"],
                "company_id": company.id,
                "currency_id": acc.get("currency_id", self.env["res.currency"]).id,
                "sequence": 10,
            }
            # Bank/cash
            account = self._l10n_nl_rgs_get_create_bank_cash_account(
                acc["account_type"], company
            )
            if account:
                vals.update({"default_account_id": account.id})
                account.deprecated = False
            new_journal = self.env["account.journal"].create(vals)
            bank_journals += new_journal
            if account:
                account.allowed_journal_ids |= new_journal

        return bank_journals

    def _l10n_nl_rgs_get_create_bank_cash_account(self, account_type, company):
        self.ensure_one()
        prefix = False
        if account_type == "bank" and self.bank_account_code_prefix:
            prefix = self.bank_account_code_prefix
        if account_type == "cash" and self.cash_account_code_prefix:
            prefix = self.cash_account_code_prefix
        digits = self.code_digits
        accounts = self.env["account.account"].search(
            [("code", "=like", prefix + "%"), ("company_id", "=", company.id)]
        )
        for num in range(0, 9):
            new_code = str(prefix.ljust(digits - 1, "0")) + str(num)
            rec = accounts.filtered(lambda a: a.code == new_code)
            if rec:
                existing_journal = self.env["account.journal"].search(
                    [
                        ("type", "=", account_type),
                        ("default_account_id", "=", rec.id),
                        ("company_id", "=", company.id),
                    ],
                    limit=1,
                )
                if not existing_journal:
                    return rec
            if not rec:
                # TODO automatically create a new account?
                # new_account = self.env["account.account"].create({"code": new_code, "company_id": company.id})
                # return new_account
                pass

    @api.model
    def _create_cash_discount_loss_account(self, company, code_digits):
        rgs_coa = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False)
        if (
            company.chart_template_id == rgs_coa
            and company.default_cash_difference_expense_account_id
        ):
            return company.default_cash_difference_expense_account_id
        return super()._create_cash_discount_loss_account(company, code_digits)

    @api.model
    def _create_cash_discount_gain_account(self, company, code_digits):
        rgs_coa = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template", False)
        if (
            company.chart_template_id == rgs_coa
            and company.default_cash_difference_income_account_id
        ):
            return company.default_cash_difference_income_account_id
        return super()._create_cash_discount_gain_account(company, code_digits)

    def _translate_journal_names_to_dutch(self, company):
        """Workaround to translate journal names to Dutch, since standard Odoo doesn't do that"""

        installed_langs = dict(self.env["res.lang"].get_installed())
        # Install Dutch language if not done yet
        lang = "nl_NL"
        if lang not in installed_langs:
            self.env["res.lang"]._activate_lang(lang)
        journals = self.env["account.journal"].search(
            [
                ("company_id", "=", company.id),
            ]
        )
        for journal in journals:
            if (
                journal.code == "INV"
                and journal.with_context(lang="en_US").name == "Customer Invoices"
            ):
                journal.update_field_translations("name", {"nl_NL": "Klantfacturen"})
            elif (
                journal.code == "BILL"
                and journal.with_context(lang="en_US").name == "Vendor Bills"
            ):
                journal.update_field_translations(
                    "name", {"nl_NL": "Leveranciersfacturen"}
                )
            elif (
                journal.code == "MISC"
                and journal.with_context(lang="en_US").name
                == "Miscellaneous Operations"
            ):
                journal.update_field_translations("name", {"nl_NL": "Memoriaal"})
            elif (
                journal.code == "EXCH"
                and journal.with_context(lang="en_US").name == "Exchange Difference"
            ):
                journal.update_field_translations(
                    "name", {"nl_NL": "Wisselkoers verschil"}
                )
            elif (
                journal.code == "CABA"
                and journal.with_context(lang="en_US").name == "Cash Basis Taxes"
            ):
                journal.update_field_translations("name", {"nl_NL": "Kasstelsel BTW"})
            elif (
                journal.code.startswith("CSH")
                and journal.with_context(lang="en_US").name == "Cash"
            ):
                journal.update_field_translations("name", {"nl_NL": "Kas"})
            elif (
                journal.code == "ACCR"
                and journal.with_context(lang="en_US").name == "Accruals"
            ):
                journal.update_field_translations(
                    "name", {"nl_NL": "Overlopende rekeningen"}
                )
            elif (
                journal.code == "DEPR"
                and journal.with_context(lang="en_US").name == "Depreciations"
            ):
                journal.update_field_translations("name", {"nl_NL": "Afschrijvingen"})
            elif (
                journal.code == "FCR"
                and journal.with_context(lang="en_US").name
                == "Foreign currency revaluation"
            ):
                journal.update_field_translations(
                    "name", {"nl_NL": "Herwaardering vreemde valuta"}
                )
            elif (
                journal.code == "WAG"
                and journal.with_context(lang="en_US").name == "Wages"
            ):
                journal.update_field_translations("name", {"nl_NL": "Lonen"})
            elif (
                journal.code == "STJ"
                and journal.with_context(lang="en_US").name == "Inventory Valuation"
            ):
                journal.update_field_translations(
                    "name", {"nl_NL": "Voorraadwaardering"}
                )
