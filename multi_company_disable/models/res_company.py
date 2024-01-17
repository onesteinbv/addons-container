from odoo import _, api, models
from odoo.exceptions import AccessError


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals_list):  # pylint: disable=method-required-super
        raise AccessError(_("Multi-company is disabled"))

    @api.ondelete(at_uninstall=False)
    def _unlink_prevent(self):
        raise AccessError(_("Multi-company is disabled"))
