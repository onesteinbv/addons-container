# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import fields, models


class AccountGroupTemplate(models.Model):
    _inherit = "account.group.template"

    # FIXME: This should be English with Dutch translation
    referentiecode = fields.Char()
    code = fields.Char()
    sort_code = fields.Char(string="Sorting code")
    rgs_basic = fields.Boolean(default=False)
    rgs_extended = fields.Boolean(default=False)
    rgs_ez = fields.Boolean(default=False)
    rgs_zzp = fields.Boolean(default=False)
    rgs_bv = fields.Boolean(default=False)
    rgs_allowed_journals_code = fields.Char()
    rgs_allowed_journals_type = fields.Char()
