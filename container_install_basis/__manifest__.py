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
        # File storage
        "fs_storage",
        "fs_attachment",
        "fs_storage_backup",
        # "container_s3",
        "sale_management",
        "website",
        "website_payment",
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
        "sale_order_amount_to_invoice",
        "sale_purchase_stock",
        "base_fontawesome",
        # Extra security
        "auth_oidc",
        "container_accessibility",
        # Accountancy
        "account_fiscal_position_vat_check",
        "account_invoice_constraint_chronology",
        "account_invoice_line_default_account",
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
        "account_statement_import_online_ponto",
        "account_statement_import_online_ponto_statement_creation_mode",
        "account_statement_import_sheet_file",
        "account_statement_import_sheet_file_sheet_mappings",
        "account_move_line_attachment_preview",
        # Accountancy extra
        "account_configuration",
        "account_invoice_overdue_reminder",
        "account_move_line_tax_editable",
        "account_move_tier_validation",
        "account_statement_import_online_paypal",
        "base_municipality",
        "base_tier_validation",
        "contract",
        "contract_payment_mode",
        "currency_rate_update",
        "digest_configuration",
        "l10n_nl_bsn",
        "mollie_subscription_ept",
        "payment_custom",
        "payment_demo",
        # Dutch localization
        "l10n_nl_rgs",
        "l10n_nl_rgs_usability",
        "l10n_nl_rgs_mis_report",
        "l10n_nl_rgs_account_financial_report",
        "l10n_nl_rgs_asset",
        "l10n_nl_bank",
        "l10n_nl_xaf_auditfile_export",
        "l10n_nl_postcode",
        "l10n_nl_tax_statement",
        "l10n_nl_tax_statement_date_range",
        "l10n_nl_tax_statement_icp",
        # Containers
        "hr_employee_firstname",
        "partner_firstname",
        "web_no_bubble",
        "base_customer_company",
        "base_customer_user",
        "base_onboarding",
        "spreadsheet_dashboard_oca",
        "spreadsheet_oca_ux",
        "partner_country_default_nl",
        "project_parent",
        # Timesheets
        "hr_timesheet_sheet",
        # Debranding
        "remove_odoo_enterprise",
        "base_import_debranding",
        "website_odoo_debranding",
        # 'support_branding',  # TODO do we need it?
        "digest_disable",
        "mollie_account_sync",
        "payment_mollie_official",
        "partner_external_map",
        "mass_mailing",
        "mass_mailing_force_dedicated_server",
        "fetchmail_notify_error_to_sender",
        "l10n_nl_hr_recruitment",
        "l10n_nl_hr_expense",
    ],
    "data": [
        # "data/res.users.role.csv",  # TODO disabled for now
    ],
    "application": True,
}
