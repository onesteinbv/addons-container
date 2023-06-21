# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Netherlands - RGS Accounting (3.5.2) with Assets',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'l10n_nl_rgs',
        'account_asset_management_template'
    ],
    'data': [
        'data/account_chart_template.xml',
        'data/account_asset_group_template.xml',
        'data/account_asset_profile_template.xml',
    ],
    "post_init_hook": "post_init_hook",
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
