# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountAccountTemplayte(models.Model):
    _inherit = 'account.account.template'

    referentiecode = fields.Char(string='Referentiecode')
