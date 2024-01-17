# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Financial Report - Netherlands - RGS Accounting (3.5.2)",
    "version": "16.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "author": "Onestein",
    "website": "http://www.onestein.eu",
    "depends": ["l10n_nl_rgs", "account_financial_report"],
    "data": ["views/account_group_views.xml"],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
