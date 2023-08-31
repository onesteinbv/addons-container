# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re
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
