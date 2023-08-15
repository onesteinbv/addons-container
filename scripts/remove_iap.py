import click
import click_odoo
from odoo.exceptions import MissingError


@click.command()
@click_odoo.env_options(default_log_level="error")
def main(env):  # We have this script because module_change_auto_install doesn't work properly with initdb (click-odoo-contrib)
    modules = ["iap"]
    click.echo("Uninstalling IAP modules...")
    iap_modules = env["ir.module.module"].search([
        ("name", "in", modules),
        ("state", "=", "installed")
    ])
    if iap_modules:
        try:
            iap_modules.button_immediate_uninstall()
        except MissingError:
            iap_modules.button_immediate_upgrade()
            iap_modules.button_immediate_uninstall()


if __name__ == '__main__':
    main()
