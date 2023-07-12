# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mail Security",
    "summary": "Let users add / edit mail servers without full admin right",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Technical Settings",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "mail",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir_model_access.xml",
        "security/ir_rule.xml",

        "views/fetchmail_server_view.xml",
        "views/ir_mail_server_view.xml",

        "menuitems.xml"
    ]
}
