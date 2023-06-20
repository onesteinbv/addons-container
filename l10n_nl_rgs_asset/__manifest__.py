# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Netherlands - RGS Accounting (3.5.2) with Assets',
    'version': '3.1',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'l10n_nl_rgs',
        'account_asset_management'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/account_chart_template.xml',
        'data/account_asset_group_template.xml',
        'data/account_asset_profile_template.xml',
    ],
    'demo': [
    ],
    "post_init_hook": "post_init_hook",
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
}
