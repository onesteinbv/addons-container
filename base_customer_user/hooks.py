# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api


def pre_init_hook(cr):
    """
    Pre-install script. Install nl_NL language pack if not already installed.
    """
    logging.getLogger("odoo.addons.base_customer_user").info(
        "Check/Install nl_NL language pack"
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    installed_langs = dict(env["res.lang"].get_installed())
    # Dutch
    lang = "nl_NL"
    if lang not in installed_langs:
        env["res.lang"]._activate_lang(lang)
    # English
    lang = "en_US"
    if lang not in installed_langs:
        env["res.lang"]._activate_lang(lang)

    # Force translation of all modules to Dutch
    mods = env["ir.module.module"].search([("state", "=", "installed")])
    mods._update_translations(["nl_NL"], True)

    # Force position of EUR currency to "before"
    currency = env["res.currency"].search([("name", "=", "EUR")])
    currency.write({"position": "before"})
