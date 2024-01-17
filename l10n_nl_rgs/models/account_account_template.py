# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import fields, models


class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"

    referentiecode = fields.Char(string="Referentiecode")
    sort_code = fields.Char(string="Sorting code")
