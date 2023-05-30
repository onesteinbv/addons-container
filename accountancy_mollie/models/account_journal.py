# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _default_outbound_payment_methods(self):
        all_out = super()._default_outbound_payment_methods()
        return all_out.filtered(lambda pm: pm.code != "mollie")

    def _default_inbound_payment_methods(self):
        all_in = super()._default_inbound_payment_methods()
        return all_in.filtered(lambda pm: pm.code != "mollie")
