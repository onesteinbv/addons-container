# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(
        self,
        domain,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        if not self.env.user.has_group(
            "base_partner_security.group_view_administrator_partner"
        ):
            partner_admin = self.env.ref("base.partner_admin")
            partner_private_address = self.env.ref(
                "hr.res_partner_admin_private_address"
            )
            domain = expression.AND(
                [
                    domain,
                    [("id", "not in", [partner_admin.id, partner_private_address.id])],
                ]
            )
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
