# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models, _


class AccountGroup(models.Model):
    _inherit = 'account.group'

    referentiecode = fields.Char(string='Referentiecode')
    code = fields.Char(string='Code')

    def _adapt_parent_account_group(self):
        if self.company_id.chart_template_id != self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            return super(AccountGroup, self)._adapt_parent_account_group()
