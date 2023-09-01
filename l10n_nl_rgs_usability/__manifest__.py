
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
        'account_move_name_sequence',
        "account_payment_order",
        "account_payment_mode",
        "account_banking_sepa_credit_transfer",
    ],
    'data': [
        'security/ir_sequence_security.xml',
        'data/account_payment_term.xml',
        'data/res_groups.xml',
        'views/account_journal_views.xml',
    ],
    'demo': [
        'demo/account_demo.xml',
    ],
    "post_init_hook": "post_init_hook",
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
