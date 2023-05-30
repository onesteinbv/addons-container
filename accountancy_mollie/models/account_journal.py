# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _payment_methods_not_default(self):
        return self.env.ref('payment_mollie.payment_method_mollie') or self.env['account.payment.method']

    def _default_outbound_payment_methods(self):
        all_out = super()._default_outbound_payment_methods()
        all_out = all_out - self._payment_methods_not_default()
        return all_out

    def _default_inbound_payment_methods(self):
        all_in = super()._default_inbound_payment_methods()
        all_in = all_in - self._payment_methods_not_default()
        return all_in

