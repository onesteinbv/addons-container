# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

{
    "name": "Netherlands - RGS Accounting (3.5.2)",
    "version": "16.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "depends": ["account", "l10n_nl", "l10n_multilang"],
    "data": [
        "data/account_account_tag.xml",
        "data/account_chart_template.xml",
        "data/account_group_template.xml",
        "data/account.account.template.csv",
        "data/account_chart_template_post_data.xml",
        "data/account_tax_group_data.xml",
        "data/account_tax_template.xml",
        "data/account_fiscal_position_template.xml",
        "data/account_fiscal_position_tax_template.xml",
        "data/account_fiscal_position_account_template.xml",
        "data/account_chart_template_data.xml",
        "views/res_config_settings_views.xml",
        "views/account_account_views.xml",
        "views/account_group_views.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
