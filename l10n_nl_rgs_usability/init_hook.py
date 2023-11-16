# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})

    companies = env['res.company'].search([])

    for company in companies:

        # Generate payment modes
        env["account.chart.template"]._generate_payment_modes(company)

    # Set payment credit account for bank journals
    journals = env['account.journal'].search([])
    journals._set_journal_bank_payment_credit_account()

    # Auto-install RGS for main company
    main_company = env.ref('base.main_company', False)
    rgs = env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False)
    if main_company and main_company.chart_template_id != rgs and not rgs.existing_accounting(main_company):
        rgs._load(main_company)

        # Installing stock_account will create ir.property property_stock_account_output_categ_id and property_stock_account_input_categ_id for the
        # main_company. Somehow if this module is installed it removes the ir.model.data or ir.property. (in rgs._load(main_company) -> self.generate_properties())
        # See: accounts/chart_template.py in def _load(self, company) it deletes ir.property
        # This is a core issue it can also be triggered by creating a database installing stock_account installing belgium coa switch to it, and update stock_account

        # TODO: Fix in core
        xml_ids = [
            ("stock_account", "property_stock_account_output_categ_id"),
            ("stock_account", "property_stock_account_input_categ_id")
        ]
        for xml_id in xml_ids:
            ir_property = env.ref("%s.%s" % (xml_id[0], xml_id[1]), False)
            if ir_property:
                continue
            env["ir.model.data"].create({
                "res_id": env["ir.property"].search([
                    ("name", "=", xml_id[1]), ("company_id", "=", main_company.id), ("res_id", "=", False)
                ]),
                "model": "ir.property",
                "name": xml_id[1],
                "module": xml_id[0],
                "noupdate": True
            })

    # Archive the cash basis tax journal
    journals = env['account.journal'].search([])
    for journal in journals.filtered(lambda j: j.code == "CABA"):
        if journal.company_id.chart_template_id == env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
            journal.active = False

    companies = env["res.company"].search([])
    for company in companies:
        # Verify VAT Numbers set to True
        company.vat_check_vies = True
        # Create Direct debit in payment mode
        company._create_direct_debit_in_payment_mode()
        # Create spread templates
        company._create_spread_templates()
