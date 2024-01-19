# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

from ..init_hook import post_init_hook


class TestRGSAsset(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.coa = cls.env.ref("l10n_nl_rgs.l10nnl_rgs_chart_template")
        cls.company_rgs = cls.env.ref("l10n_nl_rgs.demo_company_nl_rgs")
        cls.env.user.company_id = cls.company_rgs

    def test_01_data_loaded(self):
        """Company NL RGS defined in l10n_nl_rgs is loaded with asset data from template"""
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", self.company_rgs.id),
            ]
        )
        self.assertEqual(group_count, 2)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", self.company_rgs.id),
            ]
        )
        self.assertEqual(group_profile, 9)

    def test_02_post_init_hook(self):
        """Test post_init_hook"""
        # Create a company having RGS coa
        company_1 = self.env["res.company"].create(
            {
                "name": "Asset Company1",
                "chart_template_id": self.coa.id,
            }
        )
        self.env.user.company_id = company_1

        # The asset groups and asset profiles are empty
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_count, 0)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_profile, 0)

        # Load RGS coa
        self.coa._load(company_1)

        # The asset groups and asset profiles are loaded
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_count, 2)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_profile, 9)

        # Force call post_init_hook
        post_init_hook(self.cr, self.registry)

        # The asset groups and asset profiles are loaded
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_count, 2)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", company_1.id),
            ]
        )
        self.assertEqual(group_profile, 9)
