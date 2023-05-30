# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountGroupTemplate(models.Model):
    _inherit = 'account.group.template'

    referentiecode = fields.Char(string='Referentiecode')
    code = fields.Char(string='Code')
