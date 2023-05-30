# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Financial Consolidation Reports",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Onestein BV, André Schenkels",
    "category": "Accounting",
    "summary": "",
    "depends": [
        "account",
        "account_financial_report",
        "consolidation_account",
    ],
    "data": [
        'view/consolidation_account_view.xml',
        # 'report/templates/trial_balance.xml',
        'wizard/trial_balance_wizard_view.xml',
    ],
}
