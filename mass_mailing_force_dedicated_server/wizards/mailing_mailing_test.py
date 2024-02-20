from odoo import models


class MailingMailingTest(models.TransientModel):
    _inherit = "mailing.mailing.test"

    def send_mail_test(self):
        self.ensure_one()
        self.mass_mailing_id._force_dedicated_server()
        return super().send_mail_test()
