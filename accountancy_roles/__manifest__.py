# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Accountancy User Roles",
    "summary": """
        This module sets up basic user roles""",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "Onestein BV, André Schenkels",
    "website": "https://www.onestein.nl",
    "depends": [
        'account',
        'base_user_role',
    ],
    "data": [
        'data/accountancy_roles.xml',
    ],
}
