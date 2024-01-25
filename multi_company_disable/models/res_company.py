from odoo import _, api, models
from odoo.exceptions import AccessError


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.is_superuser():
            raise AccessError(_("Multi-company is disabled"))
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent(self):
        if not self.env.is_superuser():
            raise AccessError(_("Multi-company is disabled"))
