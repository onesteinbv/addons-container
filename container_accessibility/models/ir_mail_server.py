from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    private = fields.Boolean(
        string="Is private server"
    )

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None,
                   smtp_ssl_certificate=None, smtp_ssl_private_key=None,
                   smtp_debug=False, smtp_session=None):
        mail_server = self.sudo().browse(mail_server_id)  # Sudo?
        if mail_server.private and not self.env.context.get("allow_private_mail_server", False):
            raise AccessError(_("You're not allowed to use a private mail server for this email"))
        return super().send_email(
            message, mail_server_id, smtp_server, smtp_port,
            smtp_user, smtp_password, smtp_encryption,
            smtp_ssl_certificate, smtp_ssl_private_key,
            smtp_debug, smtp_session
        )

