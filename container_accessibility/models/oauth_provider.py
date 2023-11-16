from odoo import fields, models


class OauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    private = fields.Boolean()
