from odoo import api, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        model = self.with_user(access_rights_uid) if access_rights_uid else self
        if model.env.user.is_restricted_user():
            partners = (
                self.env.ref("base.partner_admin") +
                self.env.ref("hr.res_partner_admin_private_address") +
                self.env.ref("base.partner_root")
            )
            domain = expression.AND([
                domain,
                [("id", "not in", partners.ids)]
            ])
        return super()._search(
            domain, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid
        )
