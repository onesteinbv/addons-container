# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import fields, api, Command, models, _


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):

        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super(AccountChartTemplate, self)._prepare_all_journals(
                acc_template_ref, company, journals_dict=journals_dict)

        journals_dict = [
            {'name': _('Accruals'), 'type': 'general', 'code': _('ACCR'), 'favorite': True, 'color': 11, 'sequence': 15},
            {'name': _('Depreciations'), 'type': 'general', 'code': 'DEPR', 'favorite': True, 'color': 11, 'sequence': 16},
            {'name': _('Foreign currency revaluation'), 'type': 'general', 'code': _('FCR'), 'favorite': True, 'sequence': 17},
            {'name': _('Wages'), 'type': 'general', 'code': _('WAG'), 'favorite': True, 'sequence': 18},
            {'name': _('Inventory Valuation'), 'type': 'general', 'code': _('STJ'), 'favorite': True, 'sequence': 19}]
        resp_journals = super(AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict=journals_dict)
        # TODO: Remove unwanted journals
        return resp_journals

    @api.model
    def _prepare_transfer_account_for_direct_creation(self, name, company):
        res = super(AccountChartTemplate, self)._prepare_transfer_account_for_direct_creation(name, company)
        if company.account_fiscal_country_id.code == 'NL':
            xml_id = self.env.ref('l10n_nl_rgs.account_tag_1003000').id
            res.setdefault('tag_ids', [])
            res['tag_ids'].append((4, xml_id))
        return res

    @api.model
    def _create_liquidity_journal_suspense_account(self, company, code_digits):
        account = super()._create_liquidity_journal_suspense_account(company, code_digits)
        if company.account_fiscal_country_id.code == 'NL':
            account.tag_ids = [Command.link(self.env.ref('l10n_nl_rgs.account_tag_1003000').id)]
        return account

    def _get_account_vals(self, company, account_template, code_acc, tax_template_ref):
        self.ensure_one()
        vals = super()._get_account_vals(company, account_template, code_acc, tax_template_ref)

        if self == self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            vals.update({
                'referentiecode': account_template.referentiecode,
                'sort_code': account_template.sort_code})
        return vals

    def generate_account(self, tax_template_ref, acc_template_ref, code_digits, company):
        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super().generate_account(tax_template_ref, acc_template_ref, code_digits, company)

        self.ensure_one()
        account_tmpl_obj = self.env['account.account.template']
        acc_template = account_tmpl_obj.search([('nocreate', '!=', True), ('chart_template_id', '=', self.id)], order='id')
        template_vals = []
        acc_template_done = self.env["account.account.template"]
        for account_template in acc_template:
            if not account_template[company.l10n_nl_company_type] and not account_template["rgs_basic"] and not account_template["rgs_extended"]:
                continue
            acc_template_done |= account_template
            code_main = account_template.code and len(account_template.code) or 0
            code_acc = account_template.code or ''
            if code_main > 0 and code_main <= code_digits:
                code_acc = str(code_acc) + (str('0'*(code_digits-code_main)))
            vals = self._get_account_vals(company, account_template, code_acc, tax_template_ref)
            if company.l10n_nl_rgs_type != "rgs_extended" and not account_template["rgs_basic"] and account_template["rgs_extended"]:
                vals.update({
                    "deprecated": True,
                })
            template_vals.append((account_template, vals))
        accounts = self._create_records_with_xmlid('account.account', template_vals, company)
        for template, account in zip(acc_template_done, accounts):
            acc_template_ref[template] = account
        return acc_template_ref

    def generate_account_groups(self, company):
        """ Inherit this method to fix reference code missing in account groups"""
        self.ensure_one()

        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super().generate_account_groups(company)

        # Overrides standard Odoo method
        group_templates = self.env['account.group.template'].search([('chart_template_id', '=', self.id)])
        template_vals = []
        for group_template in group_templates:
            if not group_template[company.l10n_nl_company_type] and not group_template["rgs_basic"] and not group_template["rgs_extended"]:
                continue
            vals = {
                'name': group_template.name,
                'code_prefix_start': group_template.code_prefix_start,
                'code_prefix_end': group_template.code_prefix_end,
                'company_id': company.id,
                'code': group_template.code,
                'referentiecode': group_template.referentiecode,
                'sort_code': group_template.sort_code
            }
            template_vals.append((group_template, vals))

        groups = self._create_records_with_xmlid('account.group', template_vals, company)

        for group_template in group_templates.filtered(lambda agt: agt.parent_id):
            parent_group = groups.filtered(lambda ag: ag.code == group_template.parent_id.code)
            group = groups.filtered(lambda ag: ag.code == group_template.code)
            if group and parent_group:
                group.parent_id = parent_group.id

    def _load_template(self, company, code_digits=None, account_ref=None, taxes_ref=None):
        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super(AccountChartTemplate, self)._load_template(
                company, code_digits=code_digits,
                account_ref=account_ref, taxes_ref=taxes_ref)

        account_ref, taxes_ref = super(AccountChartTemplate, self)._load_template(
            company, code_digits=code_digits,
            account_ref=account_ref, taxes_ref=taxes_ref)

        # Add allowed journals to accounts based on group settings
        if not company.l10n_nl_rgs_disable_allowed_journals:
            self.add_account_allowed_journals(company)

        return account_ref, taxes_ref

    def add_account_allowed_journals(self, company):
        """ Inherit this method to fix reference code missing in account groups"""
        self.ensure_one()

        group_templates = self.env['account.group.template'].search([
            ('chart_template_id', '=', self.id),
            '|',
            ('rgs_allowed_journals_code', '!=', False),
            ('rgs_allowed_journals_type', '!=', False)])
        referentiecodes = group_templates.mapped("referentiecode")
        all_groups = self.env['account.group'].search([
            ('company_id', '=', company.id),
            ('referentiecode', 'in', referentiecodes)])
        all_journals = self.env['account.journal'].search([
            ('company_id', '=', company.id),
        ])

        for group_template in group_templates:
            group = all_groups.filtered(lambda g: g.referentiecode == group_template.referentiecode)
            if not group:
                continue
            journals = self.env['account.journal']
            if group_template.rgs_allowed_journals_type:
                type_list = [jtype for jtype in group_template.rgs_allowed_journals_type.split(",")]
                journals |= self.get_allowed_account_journals_based_on_type(all_journals, type_list)
            if group_template.rgs_allowed_journals_code:
                code_list = [jcode for jcode in group_template.rgs_allowed_journals_code.split(",")]
                journals |= self.get_allowed_account_journals_based_on_code(all_journals, code_list)

            if journals:
                accounts = group.get_all_account_ids()
                accounts.write({
                    'allowed_journal_ids': [(6, 0, journals.ids)]
                })

    def get_allowed_account_journals_based_on_type(self, all_journals, type_list):
        return all_journals.filtered(lambda j: j.type in type_list)

    def get_allowed_account_journals_based_on_code(self, all_journals, code_list):
        return all_journals.filtered(lambda j: j.code in code_list)

    def _create_bank_journals(self, company, acc_template_ref):
        self.ensure_one()
        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super()._create_bank_journals(company, acc_template_ref)

        bank_journals = self.env['account.journal']
        # Create the journals that will trigger the account.account creation
        for acc in self._get_default_bank_journals_data():
            vals = {
                'name': acc['acc_name'],
                'type': acc['account_type'],
                'company_id': company.id,
                'currency_id': acc.get('currency_id', self.env['res.currency']).id,
                'sequence': 10,
            }
            # Bank/cash
            account_code = False
            account = self.env['account.account']
            if acc['account_type'] == "bank" and self.bank_account_code_prefix:
                account_code = self.bank_account_code_prefix + "0"
            if acc['account_type'] == "cash" and self.cash_account_code_prefix:
                account_code = self.cash_account_code_prefix + "0"
            if account_code:
                account = self.env['account.account'].search([
                    ('code', '=', account_code),
                    ('company_id', '=', company.id)
                ], limit=1)
            if account:
                vals.update({"default_account_id": account.id})
            new_journal = self.env['account.journal'].create(vals)
            bank_journals += new_journal
            if account:
                account.allowed_journal_ids |= new_journal

        return bank_journals
