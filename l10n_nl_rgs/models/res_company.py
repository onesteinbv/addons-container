from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    l10n_nl_rgs_type = fields.Selection([
        ('rgs_basic', 'Basic'),
        ('rgs_extended', 'Extended'),
        ('rgs_ez', 'EZ / VOF'),
        ('rgs_zzp', 'ZZP'),
        ('rgs_bv', 'BV')
    ])
    l10n_nl_rgs_setup_allowed_journals = fields.Boolean(
        string='Setup allowed journals',
        default=False,
    )
