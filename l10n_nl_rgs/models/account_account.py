# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    referentiecode = fields.Char(string='Referentiecode')
