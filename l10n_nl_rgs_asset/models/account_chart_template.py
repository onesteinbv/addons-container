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
