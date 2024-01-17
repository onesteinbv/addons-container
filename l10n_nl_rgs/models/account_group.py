# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import fields, models


class AccountGroup(models.Model):
    _inherit = "account.group"
    _order = "sort_code, code, code_prefix_start"

    # FIXME: This should be English with Dutch translation
    referentiecode = fields.Char()
    code = fields.Char()
    sort_code = fields.Char(string="Sorting code")

    # From account financial report
    group_child_ids = fields.One2many(
        comodel_name="account.group", inverse_name="parent_id", string="Child Groups"
    )
    account_ids = fields.One2many(
        comodel_name="account.account", inverse_name="group_id", string="Accounts"
    )

    def _adapt_parent_account_group(self):
        if self.company_id.chart_template_id != self.env.ref(
            "l10n_nl_rgs.l10nnl_rgs_chart_template", False
        ):
            return super(AccountGroup, self)._adapt_parent_account_group()

    def get_all_account_ids(self):
        accounts = self.env["account.account"]
        for rec in self:
            accounts |= rec.account_ids
            if rec.group_child_ids:
                accounts |= rec.group_child_ids.get_all_account_ids()
        return accounts
