# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AgedPartnerBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.abstract_report"
