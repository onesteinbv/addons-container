from odoo import models
from odoo.exceptions import UserError


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _send(self, auto_commit=False, raise_exception=False, smtp_session=None):
        if self.mailing_id:
            try:
                self.mailing_id._force_dedicated_server()
            except UserError as e:
                if raise_exception:
                    raise e
                self.write({"state": "exception", "failure_reason": str(e)})
        return super()._send(auto_commit, raise_exception, smtp_session)
