from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_auth_oauth = fields.Boolean(readonly=True)

    def execute(self):
        return super(
            ResConfigSettings, self.with_context(no_restrict=True)
        ).execute()

