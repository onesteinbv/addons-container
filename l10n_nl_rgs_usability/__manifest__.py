
{
    'name': 'Netherlands - RGS Accounting - Usability',
    "version": "16.0.1.0.0",
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Onestein',
    'website': 'https://www.onestein.eu',
    'depends': [
        'l10n_nl_rgs',
        'base_view_inheritance_extension',
        'account_usability',
        'product_category_tax',
    ],
    'data': [
        'views/account_journal_views.xml',
    ],
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
