# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestAssetTemplate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.coa = cls.env.ref("l10n_generic_coa.configurable_chart_template")
        cls.company_1 = cls.env["res.company"].create(
            {
                "name": "Asset Company1",
            }
        )
        cls.env.user.company_id = cls.company_1

    def test_01_load_coa(self):
        """ """
        group_count = self.env['account.asset.group'].search_count([
            ('company_id', '=', self.company_1.id),
        ])
        self.assertEqual(group_count, 0)
        group_profile = self.env['account.asset.profile'].search_count([
            ('company_id', '=', self.company_1.id),
        ])
        self.assertEqual(group_profile, 0)

        self.coa.try_loading(self.company_1, install_demo=False)

        group_count = self.env['account.asset.group'].search_count([
            ('company_id', '=', self.company_1.id),
        ])
        self.assertEqual(group_count, 2)
        group_profile = self.env['account.asset.profile'].search_count([
            ('company_id', '=', self.company_1.id),
        ])
        self.assertEqual(group_profile, 9)
