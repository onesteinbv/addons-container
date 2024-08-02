from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_auth_oauth = fields.Boolean(readonly=True)

    def execute(self):
        sudo_self = self
        if self.env.user.is_restricted_user() and self.env.user.has_group(
            "base.group_system"
        ):
            sudo_self = self.sudo()
        return super(ResConfigSettings, sudo_self).execute()
