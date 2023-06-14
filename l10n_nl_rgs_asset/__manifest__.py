# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 Onestein (<http://www.onestein.eu>).

{
    'name': 'Netherlands - RGS Accounting (3.5.2) with Assets',
    'version': '16.0.1.0.0',
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
        'data/account_chart_template_data.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
}
