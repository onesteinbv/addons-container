from odoo import models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    def button_immediate_install(self):
        return super(
            PaymentProvider, self.with_context(no_restrict=True)
        ).button_immediate_install()
