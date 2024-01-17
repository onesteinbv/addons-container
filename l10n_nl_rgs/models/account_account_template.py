# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import fields, models


class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"

    # FIXME: This should be English with Dutch translation
    referentiecode = fields.Char()
    sort_code = fields.Char(string="Sorting code")
