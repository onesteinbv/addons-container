from odoo import fields, models


class OauthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    private = fields.Boolean()
    template_user_id = fields.Many2one(comodel_name="res.users")
    group_ids = fields.Many2many(comodel_name="res.groups")
