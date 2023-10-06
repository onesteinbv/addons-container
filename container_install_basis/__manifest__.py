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
        "website_sale",
        "web_responsive",
        "disable_odoo_online",
        "account_payment_mode",
        "account_payment_order",
        "account_payment_partner",
        "sale_stock",
        "payment_mollie",
        "crm",
        "hr_expense",
        "hr_expense_remove_mobile_link",
        "project_hr_expense",
        "project_purchase",
        "account_move_line_purchase_info",
        "account_move_line_sale_info",
        "account_move_line_stock_info",
        "purchase_stock",
        "sale_purchase_stock",

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
        "account_reconcile_oca",
        "account_statement_base",
        "account_payment_sale",
        "report_qr",
        "report_qweb_parameter",
        "report_wkhtmltopdf_param",
        "report_xlsx",
        "report_xlsx_helper",
        "date_range",
        "product_margin",
        "account_financial_report",
        "product_category_product_link",
        "account_statement_import_camt",
        "account_statement_import_camt54",
        "account_statement_import_file_reconcile_oca",
        "account_period_auto_create",
        "account_fiscal_year_auto_create",
        "account_statement_import_online_ponto",
        "account_move_line_attachment_preview",

        # Dutch localization
        "l10n_nl_rgs",
        "l10n_nl_rgs_usability",
        "l10n_nl_bank",
        "l10n_nl_xaf_auditfile_export",
        "l10n_nl_postcode",
        "l10n_nl_tax_statement",
        "l10n_nl_tax_statement_date_range",
        'l10n_nl_tax_statement_icp',

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
        "partner_country_default_nl",

        # Timesheets
        "hr_timesheet_sheet",

        # Debranding
        "remove_odoo_enterprise",
        "base_import_debranding",
        "website_odoo_debranding",
        # 'support_branding',  # TODO do we need it?
        "digest_disable"
    ],
    "data": [],
    "application": True,
}
