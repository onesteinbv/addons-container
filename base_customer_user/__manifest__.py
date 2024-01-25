{
    "name": "Customer User",
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    "category": "Technical Settings",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "depends": [
        "base",
        "mail",
        "mail_bot",
        "partner_firstname",
    ],  # Temporary if this fixes the issue
    "data": [
        "data/res_users_data.xml",
        "data/res_currency_data.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
