# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

from odoo import api, fields, models, _


class AccountAssetGroupTemplate(models.Model):
    _name = "account.asset.group.template"
    _inherit = ['mail.thread']
    _description = 'Templates for Asset Groups'
    _order = "code"

    name = fields.Char(size=64, required=True, index=True)
    code = fields.Char(index=True)
    chart_template_id = fields.Many2one('account.chart.template', string='Chart Template')



    
