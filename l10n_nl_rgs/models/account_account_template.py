# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models, _


class AccountAccountTemplayte(models.Model):
    _inherit = 'account.account.template'

    referentiecode = fields.Char(string='Referentiecode')
