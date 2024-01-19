# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import HttpCase


class TestL10nNlRgsMisReports(HttpCase):
    def test_01_rgs_balance_sheet(self):
        """"""
        report = "l10n_nl_rgs_mis_report.mis_report_l10n_nl_rgs_balance_sheet"
        instance = self.env["mis.report.instance"].create(
            {
                "name": "Balance Sheet",
                "report_id": self.env.ref(report).id,
            }
        )
        instance.preview()

    def test_02_rgs_profit_loss(self):
        """"""
        report = "l10n_nl_rgs_mis_report.mis_report_l10n_nl_rgs_profit_loss"
        instance = self.env["mis.report.instance"].create(
            {
                "name": "Profit Loss",
                "report_id": self.env.ref(report).id,
            }
        )
        instance.preview()
