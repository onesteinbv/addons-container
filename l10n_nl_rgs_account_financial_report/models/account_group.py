# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models


class AccountGroup(models.Model):
    _inherit = "account.group"

    # FIXME: This should be English with Dutch translation
    referentiecode = fields.Char()
    code = fields.Char()
    compute_account_ids = fields.Many2many(
        "account.account",
        compute="_compute_group_accounts",
        string="Compute accounts",
        store=True,
    )
    complete_name = fields.Char(
        "Full Name", compute="_compute_complete_name", recursive=True
    )
    complete_code = fields.Char(
        "Full Code", compute="_compute_complete_code", recursive=True
    )

    def _adapt_parent_account_group(self):
        if self.company_id.chart_template_id != self.env.ref(
            "l10n_nl_rgs.l10nnl_rgs_chart_template", False
        ):
            return super(AccountGroup, self)._adapt_parent_account_group()

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        if self.company_id.chart_template_id != self.env.ref(
            "l10n_nl_rgs.l10nnl_rgs_chart_template", False
        ):
            return super(AccountGroup, self)._compute_complete_name()
        for group in self:
            group.complete_name = group.name

    @api.depends("code_prefix_start", "parent_id.complete_code", "code")
    def _compute_complete_code(self):
        if self.company_id.chart_template_id != self.env.ref(
            "l10n_nl_rgs.l10nnl_rgs_chart_template", False
        ):
            return super(AccountGroup, self)._compute_complete_code()
        for group in self:
            group.complete_code = group.code

    @api.depends(
        "code_prefix_start",
        "account_ids",
        "account_ids.code",
        "group_child_ids",
        "group_child_ids.account_ids.code",
        "code",
    )
    def _compute_group_accounts(self):
        if self.company_id.chart_template_id != self.env.ref(
            "l10n_nl_rgs.l10nnl_rgs_chart_template", False
        ):
            return super(AccountGroup, self)._compute_group_accounts()
        for group in self:
            gr_accounts = group.get_all_account_ids()
            group.compute_account_ids = [(6, 0, gr_accounts.ids)]
