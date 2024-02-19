# Copyright (C) 2024 Onestein (<http://www.onestein.eu>).
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class L10nNlRGSCoa(TransactionCase):
    def setUp(self):
        super().setUp()
        self.l10n_nl_rgs_coa = self.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        self.l10n_nl_rgs_company = self.env["res.company"].create(
            {"name": "Test Company"}
        )

    def test_l10n_nl_rgs_coa(self):
        """Test installing the chart of accounts template in a new company"""
        self.l10n_nl_rgs_coa._load(company=self.l10n_nl_rgs_company)
        self.assertEqual(
            self.l10n_nl_rgs_coa, self.l10n_nl_rgs_company.chart_template_id
        )
