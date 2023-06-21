# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Asset management template',
    'version': '16.0.1.0.0',
    "category": "Accounting & Finance",
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'account_asset_management',
        'l10n_generic_coa',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/account_asset_group_template.xml',
        'demo/account_asset_profile_template.xml',
    ],
    'license': 'LGPL-3',
}
