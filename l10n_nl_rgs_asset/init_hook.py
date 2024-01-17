# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})

    chart_template = env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
    companies = env["res.company"].search(
        [
            ("chart_template_id", "child_of", chart_template.id),
        ]
    )

    for company in companies:
        # Generate Asset Groups from Templates
        asset_group_ref = chart_template.generate_account_asset_groups(company)

        # Generate Asset Profiles from Templates
        chart_template.generate_account_asset_profile(asset_group_ref, company)
