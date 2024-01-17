from odoo import models


class FSStorage(models.Model):
    _inherit = "fs.storage"

    def backup_db(self):
        return super(
            FSStorage, self.with_context(allow_private_mail_server=True)
        ).backup_db()

    def cleanup_old_backups(self):
        return super(
            FSStorage, self.with_context(allow_private_mail_server=True)
        ).cleanup_old_backups()
