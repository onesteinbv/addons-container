from odoo import _, models
from odoo.exceptions import AccessError


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_immediate_install(self):
        if self.env.user.is_restricted_user() and not self.env.context.get("install_payment_provider", False):
            raise AccessError(_("Access denied to install modules"))
        return super().button_immediate_install()

    def button_immediate_upgrade(self):
        if self.env.user.is_restricted_user():
            raise AccessError(_("Access denied to update modules"))
        return super().button_immediate_upgrade()

    def button_immediate_uninstall(self):
        if self.env.user.is_restricted_user():
            raise AccessError(_("Access denied to uninstall modules"))
        return super().button_immediate_uninstall()
