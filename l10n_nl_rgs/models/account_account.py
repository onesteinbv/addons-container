# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).
from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"
    _order = "is_off_balance, sort_code, code, company_id"

    # FIXME: This should be English with Dutch translation
    referentiecode = fields.Char()
    sort_code = fields.Char(string="Sorting code")

    def write(self, vals):
        resp = super(AccountAccount, self).write(vals)

        for rec in self.filtered(
            lambda acc: not acc.referentiecode
            and acc.group_id
            and acc.group_id.referentiecode
        ):
            rec.referentiecode = rec.group_id.referentiecode

        return resp
