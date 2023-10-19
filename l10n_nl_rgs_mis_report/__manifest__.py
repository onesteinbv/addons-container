# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'MIS Reports - Netherlands - RGS Accounting (3.5.2)',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'depends': [
        'l10n_nl_rgs',
        'mis_builder'
    ],
    "data": [
        "data/mis_report_styles.xml",
        "data/mis_report_balance_sheet.xml",
        "data/mis_report_profit_loss.xml",
        "views/mis_report_instance.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
