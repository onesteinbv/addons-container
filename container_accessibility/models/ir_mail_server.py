from odoo import fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    private = fields.Boolean(string="Is private server")

    def _find_mail_server(self, email_from, mail_servers=None):
        mail_server, res_email_from = super()._find_mail_server(
            email_from, mail_servers
        )
        if (
            mail_server is not None
            and mail_server.private
            and not self.env.context.get("allow_private_mail_server", False)
        ):
            mail_servers = self.sudo().search(
                [("private", "=", False)], order="sequence"
            )
            return super()._find_mail_server(email_from, mail_servers)
        return mail_server, res_email_from
