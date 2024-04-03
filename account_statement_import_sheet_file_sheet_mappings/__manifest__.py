# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Bank Statement TXT/CSV/XLSX Import Sheet Mappings",
    "summary": "Adds sheet mappings for bank statement imports",
    "version": "16.0.1.1.0",
    "category": "Accounting",
    "website": "https://www.onestein.eu",
    "author": "Onestein",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_statement_import_sheet_file",
    ],
    "data": [
        "data/map_data.xml",
    ],
}
