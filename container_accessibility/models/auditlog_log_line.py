from odoo import _, api, models
from odoo.exceptions import AccessError


class AuditlogLogLine(models.Model):
    _inherit = "auditlog.log.line"

    def write(self, vals):
        if not self.env.context.get("auditlog_allow_crud", False):
            raise AccessError(_("Access denied"))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("auditlog_allow_crud", False):
            raise AccessError(_("Access denied"))
        return super().create(vals_list)

    def unlink(self):
        if not self.env.context.get("auditlog_allow_crud", False):
            raise AccessError(_("Access denied"))
        return super().unlink()
