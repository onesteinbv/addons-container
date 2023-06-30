# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models, _


class AccountAccountTemplate(models.Model):
    _inherit = 'account.account.template'

    referentiecode = fields.Char(string='Referentiecode')
    sort_code = fields.Char(string='Sorting code')
    rgs_basic = fields.Boolean(default=False)
    rgs_extended = fields.Boolean(default=False)
    rgs_ez = fields.Boolean(default=False)
    rgs_zzp = fields.Boolean(default=False)
    rgs_bv = fields.Boolean(default=False)