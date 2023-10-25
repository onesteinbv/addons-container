# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Trade Based Organization - Install',
    'description': 'Trade Based Organization - Install',
    'category': 'Technical Settings',
    'version': '16.0.1.0.0',
    'author': 'Onestein',
    'website': 'https://www.onestein.nl',
    'license': 'AGPL-3',
    'depends': [
        'container_install_standard',

        # Base
        'account',
        'account_edi',
        'account_edi_ubl_cii',
        'account_payment',
        'account_qr_code_sepa',
        'analytic',
        'association',
        'attachment_indexation',
        'auth_signup',
        'auth_totp',
        'auth_totp_mail',
        'auth_totp_portal',
        'barcodes',
        'base_address_extended',
        'base_automation',
        'base_geolocalize',
        'base_iban',
        'base_import',
        'base_setup',
        'base_vat',
        'board',
        'calendar',
        'calendar_sms',
        'contacts',
        'loyalty',
        'crm',
        'crm_sms',
        'event',
        'event_crm',
        'event_crm_sale',
        'event_sale',
        'event_sms',
        'google_recaptcha',
        'hr',
        'hr_contract',
        'hr_expense',
        'hr_org_chart',
        'hr_recruitment',
        'hr_timesheet',
        'http_routing',
        'l10n_nl',
        'link_tracker',
        'mail',
        'mail_bot',
        'mail_bot_hr',
        'mass_mailing',
        'mass_mailing_crm',
        'mass_mailing_event',
        'mass_mailing_event_track',
        'mass_mailing_sale',
        'payment',
        'payment_demo',
        'payment_custom',
        'phone_validation',
        'portal',
        'portal_rating',
        'product',
        'product_margin',
        'project',
        'project_hr_expense',
        'project_purchase',
        'purchase',
        'purchase_stock',
        'rating',
        'resource',
        'sale',
        'sale_loyalty',
        'sale_crm',
        'sale_expense',
        'sale_management',
        'sale_project',
        'sale_purchase',
        'sale_purchase_stock',
        'sale_sms',
        'sale_stock',
        'sales_team',
        'sms',
        'snailmail',
        'snailmail_account',
        'social_media',
        'stock',
        #'stock_account',
        'stock_sms',
        'uom',
        'utm',
        'web_editor',
        'web_kanban_gauge',
        'web_tour',
        'web_unsplash',
        'website',
        'website_blog',
        'website_crm',
        'website_crm_partner_assign',
        'website_crm_sms',
        'website_customer',
        'website_event',
        'website_event_crm',
        'website_event_sale',
        'website_event_track',
        'website_form_project',
        'website_google_map',
        'website_hr_recruitment',
        'website_links',
        'website_mail',
        'website_mass_mailing',
        'website_partner',
        'website_payment',
        'website_sale',
        'website_sale_loyalty',
        'website_sale_stock',
        'website_sms',

        # Community
        'account_reconcile_oca',
        'website_analytics_matomo',
        'account_statement_import_file_reconcile_oca',
        'account_statement_import_camt',
        'account_statement_import_online',
        'account_statement_import_online_ponto',
        'partner_external_map',
        'project_role',
        #'web_widget_dropdown_dynamic',
        'web_responsive',
        'website_odoo_debranding',
        'hr_expense_remove_mobile_link',

        # Onestein
        'base_municipality',
        'mass_mailing_help',
        'website_event_share_filter_option',
        'website_hide_navbar_technical',
        'website_project',
        'website_sale_share_filter_option',
        'website_share_blogger',
        'website_share_diaspora',
        'website_share_filter_option_blogger',
        'website_share_filter_option_diaspora',
        'website_share_filter_option_friendica',
        'website_share_filter_option_mastodon',
        'website_share_filter_option_pleroma',
        'website_share_filter_option_reddit',
        'website_share_filter_option_skype',
        'website_share_filter_option_snapchat',
        'website_share_filter_option_technical',
        'website_share_filter_option_telegram',
        'website_share_filter_option_tumblr',
        'website_share_filter_option_wordpress',
        'website_share_friendica',
        'website_share_mastodon',
        'website_share_pleroma',
        'website_share_reddit',
        'website_share_skype',
        'website_share_snapchat',
        'website_share_telegram',
        'website_share_tumblr',
        'website_share_wordpress',
        'website_snippet_dynamic_link',
        'website_snippet_openstreetmap',
        'website_two_steps_share_technical',
    ],
    'data': [],
}
