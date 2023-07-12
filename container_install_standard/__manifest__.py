# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Container - Install Medium",
    "summary": "Medium flavored modules required for Containers",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "category": "Technical Settings",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "container_install_basis",

        # Timesheets
        "hr_timesheet_sheet",

        # Dutch localization
        "l10n_nl_postcode",
        "l10n_nl_tax_statement",
        "l10n_nl_tax_statement_date_range",
        'l10n_nl_tax_statement_icp',

        # Accountancy
        "account_financial_report",
        "product_category_product_link",
        "account_statement_import_camt",
        "account_statement_import_camt54",
        "account_statement_import_file_reconcile_oca",
    ],
    "data": [],
    "application": True,
}
