# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, Command, models, _


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
        if account_template.referentiecode:
            vals.update({'referentiecode': account_template.referentiecode})
        return vals

    def generate_account_groups(self, company):
        """ Inherit this method to fix reference code missing in account groups"""
        self.ensure_one()

        if self != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super().generate_account_groups(company)

        # Overrides standard Odoo method
        group_templates = self.env['account.group.template'].search([('chart_template_id', '=', self.id)])
        template_vals = []
        for group_template in group_templates:
            vals = {
                'name': group_template.name,
                'code_prefix_start': group_template.code_prefix_start,
                'code_prefix_end': group_template.code_prefix_end,
                'company_id': company.id,
                'code': group_template.code,
                'referentiecode': group_template.referentiecode
            }
            template_vals.append((group_template, vals))
        groups = self._create_records_with_xmlid('account.group', template_vals, company)
