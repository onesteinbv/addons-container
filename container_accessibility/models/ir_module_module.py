from odoo import _, models
from odoo.exceptions import AccessError


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_immediate_install(self):
        if not self.env.user.is_restricted_user() or self.env.context.get("no_restrict", False):
            return super().button_immediate_install()
        raise AccessError(_("Access denied to install modules"))

    def button_immediate_upgrade(self):
        if not self.env.user.is_restricted_user() or self.env.context.get("no_restrict", False):
            return super().button_immediate_upgrade()
        raise AccessError(_("Access denied to update modules"))

    def button_immediate_uninstall(self):
        if not self.env.user.is_restricted_user() or self.env.context.get("no_restrict", False):
            return super().button_immediate_uninstall()
        raise AccessError(_("Access denied to uninstall modules"))
