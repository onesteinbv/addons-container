# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, Command, models, _


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _load_template(self, company, code_digits=None, account_ref=None, taxes_ref=None):
        self.ensure_one()
        if not code_digits:
            code_digits = self.code_digits

        account_ref, taxes_ref = super(AccountChartTemplate, self)._load_template(
            company, code_digits=code_digits,
            account_ref=account_ref, taxes_ref=taxes_ref)

        # Generate Asset Groups from Templates
        asset_group_ref = self.generate_account_asset_groups(company)

        # Generate Asset Profiles from Templates
        self.generate_account_asset_profile(
            asset_group_ref, account_ref, company)

        return account_ref, taxes_ref

    def generate_account_asset_groups(self, company):
        self.ensure_one()
        asset_group_ref = {}
        group_templates = self.env['account.asset.group.template'].search(
            [('chart_template_id', '=', self.id)])
        template_vals = []
        for group_template in group_templates:
            vals = {
                'name': group_template.name,
                'code': group_template.code
            }
            template_vals.append((group_template, vals))
        groups = self._create_records_with_xmlid(
            'account.asset.group', template_vals, company)
        
        for template, group in zip(group_templates, groups):
            asset_group_ref[template] = group
        return asset_group_ref

    def generate_account_asset_profile(self, asset_group_ref, account_ref, company):
        self.ensure_one()
        profiles = self.env['account.asset.profile.template'].search(
            [('chart_template_id', '=', self.id)])

        # first create fiscal positions in batch
        template_vals = []
        for profile in profiles:
            vals = {
                'name': profile.name,
                'account_asset_id': account_ref[profile.account_asset_id].id,
                'account_expense_depreciation_id': account_ref[profile.account_expense_depreciation_id].id,
                'account_depreciation_id': account_ref[profile.account_depreciation_id].id,
                'group_ids': [asset_group_ref[group].id for group in profile.group_ids],
                'days_calc': profile.days_calc,
                'asset_product_item': profile.asset_product_item,
                'method_number': profile.method_number,
                'method_period': profile.method_period,
                'method_time': profile.method_time,
                'method_progress_factor': profile.method_progress_factor,
                'note': profile.note
            }
            if profile.journal_code:
                journal = self.env['account.journal'].search([
                    ('code', '=', profile.journal_code),
                    ('company_id', '=', company.id)])
                if journal:
                    vals['journal_id'] = journal.id
            template_vals.append((profile, vals))
        self._create_records_with_xmlid(
            'account.asset.profile', template_vals, company)

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
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
        if account_template.referentiecode:
            vals.update({'referentiecode': account_template.referentiecode})
        return vals