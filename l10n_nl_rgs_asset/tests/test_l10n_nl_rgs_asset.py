# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestRGSAsset(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.coa = cls.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        cls.company_rgs = cls.env.ref("l10n_nl_rgs.demo_company_nl_rgs")
        cls.env.user.company_id = cls.company_rgs

    def test_01_data_loaded(self):
        """ """
        group_count = self.env['account.asset.group'].search_count([
            ('company_id', '=', self.company_rgs.id),
        ])
        self.assertEqual(group_count, 2)
        group_profile = self.env['account.asset.profile'].search_count([
            ('company_id', '=', self.company_rgs.id),
        ])
        self.assertEqual(group_profile, 9)
