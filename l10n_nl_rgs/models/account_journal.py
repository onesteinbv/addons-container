# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _prepare_liquidity_account_vals(self, company, code, vals):
        account_vals = super()._prepare_liquidity_account_vals(company, code, vals)

        if company.account_fiscal_country_id.code == 'NL':
            account_vals.setdefault('tag_ids', [])
            account_vals['tag_ids'].append((4, self.env.ref('l10n_nl_rgs.account_tag_1003000').id))

        return account_vals
