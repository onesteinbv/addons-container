from odoo import _, api, models
from odoo.exceptions import AccessError


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals_list):
        raise AccessError(_("Multi-company is disabled"))

    def unlink(self):
        raise AccessError(_("Multi-company is disabled"))
