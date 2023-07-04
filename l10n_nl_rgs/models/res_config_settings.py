# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rgs_type = fields.Selection(
        related='chart_template_id.rgs_type',
        string='RGS Type',
        readonly=False)
