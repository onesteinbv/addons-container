# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Accountancy Install",
    "summary": """
        This module installs all default Accountancy modules""",
    "version": "15.0.1.0.2",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "author": "Onestein BV, André Schenkels",
    "website": "https://www.onestein.nl",
    "depends": [
        # PREOCA?
        'l10n_nl_rgs',

        # BASE
        
        'payment_mollie',
        'sale_stock',
        'sale_management',

        # COMMUNITY
        # OCA account-financial-reporting
        'account_financial_report',
        # OCA account-financial-tools
        'account_asset_management',
        'account_asset_management_menu',
        'account_balance_line',
        'account_fiscal_position_vat_check',
        'account_fiscal_year',
        'account_invoice_constraint_chronology',
        'account_journal_lock_date',
        'account_lock_date_update',
        'account_move_force_removal',
        'account_move_line_menu',
        'account_move_line_purchase_info',
        'account_move_line_sale_info',
        'account_move_line_tax_editable',
		'account_move_name_sequence',
        'account_move_print',
        'account_usability',
        'base_vat_optional_vies',
        'product_category_tax',
        # OCA account-invoicing
        'account_move_tier_validation',
        'account_move_tier_validation_forward',
        # OCA account-reconcile
        'account_reconciliation_widget',
        # OCA bank-payment
	    'account_banking_pain_base',
	    'account_banking_sepa_credit_transfer',
        'account_banking_sepa_direct_debit',
        'account_payment_sale',
        # OCA bank-statement-import
		'account_statement_import_camt',
	    'account_statement_import_camt54',
	    'account_statement_import_online_ponto',
        # OCA credit-control
        'account_invoice_overdue_reminder',
        # OCA currency
        'currency_rate_update',
        # OCA l10n-netherlands
        'l10n_nl_bank',
	    'l10n_nl_bsn',
	    'l10n_nl_postcode',
        'l10n_nl_tax_statement',
        # OCA mis-builder
	    'mis_builder',
		'mis_builder_budget',
        # OCA product-attribute
        'product_category_product_link',
        # OCA reporting-engine
	    'report_qr',
	    'report_qweb_parameter',
	    'report_wkhtmltopdf_param',
        'report_xlsx',
	    'report_xlsx_helper',
        # OCA server-brand
        'disable_odoo_online',
        'remove_odoo_enterprise',
        # OCA server-tools
        'base_fontawesome',
        # OCA server-ux
        'date_range',
        # OCA stock-logistics-warehouse
        'account_move_line_stock_info',
        # OCA web
        'web_no_bubble',
        'web_responsive',
        'web_search_with_and',

        # CUSTOM
        # 'consolidation_account',
        # 'account_financial_consolidation_report',
        'accountancy_mollie',

        # PRE-OCA
        'account_statement_import_online_paypal',

        # THIRD-PARTY
        'mollie_account_sync',
        'payment_mollie_official',

    ],
    "data": [],
}
