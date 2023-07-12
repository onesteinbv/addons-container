# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Patch Password Security",
    "summary": "Customize password security requirements for a kubernetes limitation.",
    "version": "16.0.1.0.0",
    "author": "Onestein",
    "category": "Base",
    "depends": [
        "password_security",
    ],
    "license": "LGPL-3",
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
