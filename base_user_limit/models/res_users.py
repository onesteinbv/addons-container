from odoo import _, api, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_user_limit(self):
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_user_limit.limit", "0")
        )

    @api.model
    def _get_limit_excluded_users(self):
        # Note: Public user, OdooBot and user templates are archived
        portal_group = self.env.ref("base.group_portal")
        portal_users = self.search([("groups_id", "in", [portal_group.id])])
        admin_user = self.env.ref("base.user_admin")
        return (admin_user + portal_users).ids

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        limit = self._get_user_limit()
        if limit:
            self._check_user_limit_exceeded()
        return res

    def write(self, vals):
        res = super().write(vals)
        if (
            "active" in vals and vals["active"]
        ):  # If trying to activate / unarchive a user
            limit = self._get_user_limit()
            if limit:
                self._check_user_limit_exceeded()
        return res

    def _check_user_limit_exceeded(self):
        user_count = self.search(
            [("id", "not in", self._get_limit_excluded_users())], count=True
        )
        if user_count > self._get_user_limit():
            raise UserError(_("User limit exceeded"))
