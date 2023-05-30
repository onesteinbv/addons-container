# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountGroup(models.Model):
    _inherit = 'account.group'

    referentiecode = fields.Char(string='Referentiecode')
    code = fields.Char(string='Code')
