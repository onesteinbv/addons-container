# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Accountancy Install",
    "summary": """
        This module installs all default Accountancy modules""",
    "version": "16.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "Onestein BV, André Schenkels",
    "website": "https://www.onestein.eu",
    "depends": [
        "account_configuration",
        "container_install_standard",
        # PREOCA?
        "l10n_nl_rgs",
        "l10n_nl_rgs_account_financial_report",
        "l10n_nl_rgs_asset",
        "l10n_nl_rgs_mis_report",
        # BASE
        "payment_mollie",
        "sale_stock",
        "sale_management",
        # COMMUNITY
        # OCA account-financial-reporting
        "account_financial_report",
        # OCA account-financial-tools
        "account_asset_management",
        "account_spread_cost_revenue",
        "account_fiscal_position_vat_check",
        "account_invoice_constraint_chronology",
        "account_journal_lock_date",
        "account_lock_date_update",
        "account_move_line_purchase_info",
        "account_move_line_sale_info",
        "account_move_line_tax_editable",
        "account_move_print",
        "account_usability",
        "base_vat_optional_vies",
        # OCA account-invoicing
        "account_move_tier_validation",
        # OCA account-reconcile
        "account_reconcile_oca",
        # OCA bank-payment
        "account_banking_pain_base",
        "account_banking_sepa_credit_transfer",
        "account_banking_sepa_direct_debit",
        "account_payment_sale",
        # OCA bank-statement-import
        "account_statement_import_camt",
        "account_statement_import_camt54",
        "account_statement_import_online_paypal",
        "account_statement_import_online_ponto",
        "account_statement_import_sheet_file",
        # OCA credit-control
        "account_invoice_overdue_reminder",
        # OCA currency
        "currency_rate_update",
        # OCA l10n-netherlands
        "l10n_nl_bank",
        "l10n_nl_bsn",
        "l10n_nl_postcode",
        "l10n_nl_tax_statement",
        "l10n_nl_tax_statement_date_range",
        "l10n_nl_tax_statement_icp",
        "l10n_nl_xaf_auditfile_export",
        # OCA mis-builder
        "mis_builder",
        "mis_builder_budget",
        # OCA product-attribute
        "product_category_product_link",
        # OCA reporting-engine
        "report_qr",
        "report_qweb_parameter",
        "report_wkhtmltopdf_param",
        "report_xlsx",
        "report_xlsx_helper",
        # OCA server-brand
        "disable_odoo_online",
        "remove_odoo_enterprise",
        # OCA server-tools
        # OCA server-ux
        "date_range",
        # OCA stock-logistics-warehouse
        "account_move_line_stock_info",
        # OCA web
        "web_no_bubble",
        "web_responsive",
        "web_search_with_and",
        # THIRD-PARTY
        "mollie_account_sync",
        "payment_mollie_official",
    ],
    "data": [],
}
