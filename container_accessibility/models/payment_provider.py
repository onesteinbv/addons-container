from odoo import models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    def button_immediate_install(self):
        return super(PaymentProvider, self.with_context(install_payment_provider=True)).button_immediate_install()
