from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def execute(self):
        return super(
            ResConfigSettings, self.with_context(no_restrict=True)
        ).execute()

