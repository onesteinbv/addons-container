from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    check_chronology = fields.Boolean(default=True)
