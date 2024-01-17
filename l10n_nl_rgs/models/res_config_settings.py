# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_l10n_nl_rgs = fields.Boolean(
        compute="_compute_is_l10n_nl_rgs",
    )
    l10n_nl_rgs_disable_allowed_journals = fields.Boolean(
        related="company_id.l10n_nl_rgs_disable_allowed_journals",
        readonly=False,
    )

    @api.depends("chart_template_id")
    def _compute_is_l10n_nl_rgs(self):
        for config in self:
            if config.chart_template_id == self.env.ref(
                "l10n_nl_rgs.l10nnl_rgs_chart_template"
            ):
                config.is_l10n_nl_rgs = True
            else:
                config.is_l10n_nl_rgs = False
