# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    consolidation_account_ids = fields.Many2many(
        comodel_name="consolidation.account",
        string="Consolidation Accounts",
        compute="_compute_consolidation_account_ids",
        inverse="_inverse_consolidation_account_ids",
        store=True)

    @api.onchange("account_id")
    def _onchange_account_id(self):
        super()._onchange_account_id()
        if self.account_id:
            self.consolidation_account_ids = self.account_id.consolidation_account_ids

    def _compute_consolidation_account_ids(self):
        for rec in self:
            if rec.account_id and rec.account_id.consolidation_account_ids:
                rec.consolidation_account_ids = rec.account_id.consolidation_account_ids

    def _inverse_consolidation_account_ids(self):
        return

    @api.onchange("consolidation_account_ids")
    def _onchange_consolidation_account_ids(self):
        res = {}
        if self.consolidation_account_ids:
            res["domain"] = {
                "account_id": [
                    ("id", "in", self.mapped('consolidation_account_ids.account_ids').ids),
                    ("company_id", "=", self.move_id.company_id.id),
                    ("deprecated", "=", False),
                ]
            }
        else:
            res["domain"] = {
                "account_id": [
                    ("company_id", "=", self.move_id.company_id.id),
                    ("deprecated", "=", False),
                ]
            }
        return res
