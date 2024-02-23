from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.config_parameter"].search(
        [("key", "=", "digest.default_digest_emails")]
    ).unlink()
