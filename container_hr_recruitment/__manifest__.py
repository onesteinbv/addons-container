# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Container hr_recruitment patch",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "category": "Technical Settings",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_recruitment"
    ],
    "data": [
        "views/res_config_settings_view.xml"
    ],
    "installable": False   # Fixed in Odoo core https://github.com/odoo/odoo/commit/ef6f903dac4d1ca94d2c480e7f93239897397d1d
}
