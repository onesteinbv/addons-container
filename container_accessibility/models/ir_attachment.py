from odoo import models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def open(
        self,
        mode="rb",
        block_size=None,
        cache_options=None,
        compression=None,
        new_version=True,
        **kwargs,
    ):
        # TODO: Fix this upstream also make AttachmentFileLikeAdapter AbstractModel so it's inheritable by other modules.
        self.ensure_one()
        self.check("read")
        return super(IrAttachment, self.sudo()).open(
            mode, block_size, cache_options, compression, new_version, **kwargs
        )
