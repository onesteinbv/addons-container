from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    l10n_nl_rgs_disable_allowed_journals = fields.Boolean(
        string="Disable allowed journals",
        default=False,
    )
