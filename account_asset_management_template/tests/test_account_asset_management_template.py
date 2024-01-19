# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.modules.module import get_module_resource
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import convert_file


@tagged("post_install_l10n", "post_install", "-at_install")
class TestAssetTemplate(TransactionCase):
    def _load(self, *args):
        module = "account_asset_management_template"
        convert_file(
            self.cr,
            filename=get_module_resource(module, *args),
            module=module,
            idref={},
            mode="init",
            noupdate=False,
            kind="test",
        )

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
        """When try_loading a COA, the related asset groups and asset profiles are
        loaded from the templates"""
        # Load asset group templates and asset profile templates
        self._load("tests", "account_asset_group_template.xml")
        self._load("tests", "account_asset_profile_template.xml")

        # The asset groups and asset profiles are empty
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", self.company_1.id),
            ]
        )
        self.assertEqual(group_count, 0)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", self.company_1.id),
            ]
        )
        self.assertEqual(group_profile, 0)

        # Load COA
        self.coa.try_loading(self.company_1, install_demo=False)

        # The asset groups and asset profiles are loaded
        group_count = self.env["account.asset.group"].search_count(
            [
                ("company_id", "=", self.company_1.id),
            ]
        )
        self.assertEqual(group_count, 2)
        group_profile = self.env["account.asset.profile"].search_count(
            [
                ("company_id", "=", self.company_1.id),
            ]
        )
        self.assertEqual(group_profile, 9)
