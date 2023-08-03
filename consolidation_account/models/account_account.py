# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    consolidation_account_ids = fields.Many2many(
        comodel_name="consolidation.account",
        relation="account_consolidation_account_rel",
        column1='account_id',
        column2='consolidation_account_id',
        string="Consolidation Accounts",
        help="Select the consolidation accounts that should be used for this account.")

    