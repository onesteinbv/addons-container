# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Container - Install Basis",
    "summary": "Install the basic modules required for Containers",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "category": "Technical Settings",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "website",
        "web_responsive",
        "disable_odoo_online",
        "account_payment_mode",
        "account_payment_order",
        "account_payment_partner",

        # Extra security
        "website_security",
        "base_user_management",
        "base_company_management",

        # Accountancy
        "account_fiscal_position_vat_check",
        "account_fiscal_year",
        "account_invoice_constraint_chronology",
        "account_journal_lock_date",
        "account_lock_date_update",
        "account_move_print",
        "account_usability",
        "base_vat_optional_vies",
        "product_category_tax",
        "account_reconcile_oca",
        "account_statement_base",
        "account_payment_sale",
        "report_qr",
        "report_qweb_parameter",
        "report_wkhtmltopdf_param",
        "report_xlsx",
        "report_xlsx_helper",
        "date_range",

        # Dutch localization
        "l10n_nl_rgs",
        "l10n_nl_bank",
        "l10n_nl_xaf_auditfile_export",

        # Containers
        "hr_employee_firstname",
        "partner_firstname",
        "web_no_bubble",
        'base_customer_company',
        'base_customer_user',
        'base_partner_security',
        'base_mail_security',
        'base_onboarding',
        "container_hr_recruitment",
        "spreadsheet_dashboard_oca",

        "crm",

        # Debranding
        "remove_odoo_enterprise",
        "base_import_debranding",
        "website_odoo_debranding",
        # 'support_branding',  # TODO do we need it?
    ],
    "data": [],
    "application": True,
}
