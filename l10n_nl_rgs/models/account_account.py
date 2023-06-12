# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).
from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    referentiecode = fields.Char(string='Referentiecode')

    def write(self, vals):
        resp = super(AccountAccount, self).write(vals)
        
        for rec in self.filtered(lambda acc: not acc.referentiecode and acc.group_id and acc.group_id.referentiecode):
            rec.referentiecode = rec.group_id.referentiecode
        