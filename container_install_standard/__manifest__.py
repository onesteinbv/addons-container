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

        #"mass_mailing",
        #"curq_mass_mailing",

        #"sale_expense",
        #"mis_builder",

        # Timesheets
        #"sale_timesheet",
        "hr_timesheet_sheet",

        # Unece
        #"base_unece",
        #"uom_unece",
        #"account_payment_unece",
        #"account_tax_unece",
        #"l10n_nl_account_tax_unece",

        # Accountancy
        "account_asset_management",
        "currency_rate_update",
        "product_category_product_link",
        "account_statement_import_camt",
        "account_statement_import_camt54",
        "account_statement_import_file_reconcile_oca",
    ],
    "data": [],
    "application": True,
}
