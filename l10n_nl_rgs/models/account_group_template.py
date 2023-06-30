# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models, _


class AccountGroupTemplate(models.Model):
    _inherit = 'account.group.template'

    referentiecode = fields.Char(string='Referentiecode')
    code = fields.Char(string='Code')
    sort_code = fields.Char(string='Sorting code')
    rgs_basic = fields.Boolean(default=False)
    rgs_extended = fields.Boolean(default=False)
    rgs_ez = fields.Boolean(default=False)
    rgs_zzp = fields.Boolean(default=False)
    rgs_bv = fields.Boolean(default=False)
    rgs_allowed_journals_code = fields.Char()
    rgs_allowed_journals_type = fields.Char()
