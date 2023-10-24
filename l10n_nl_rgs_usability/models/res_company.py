from odoo import api, models, fields, _
from odoo import SUPERUSER_ID
from datetime import datetime


class Company(models.Model):
    _inherit = "res.company"

    vat_check_vies = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        rgs = self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False)
        for company in companies:
            if not company.chart_template_id and rgs:
                rgs.with_user(SUPERUSER_ID)._load(company)

        return companies

    def get_unaffected_earnings_account(self):
        rgs = self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False)
        if rgs:
            self = self.with_user(SUPERUSER_ID)
        return super(Company, self).get_unaffected_earnings_account()

    def _create_fiscal_year_for_current_year(self):
        self.ensure_one()
        last_fiscal_year = self.env["account.fiscal.year"].search(
            [("company_id", "=", self.id)], limit=1
        )
        year_str = '%s' % (datetime.now().year)
        date_from = fields.Date.from_string(year_str + '-01-01')
        date_to = fields.Date.from_string(year_str + '-12-31')
        if not last_fiscal_year:
            self.env["account.fiscal.year"].create({
                "name": _(
                    "FY %(date_to)s - %(date_from)s",
                    date_to=str(date_to),
                    date_from=str(date_from),
                ),
                "company_id": self.id,
                "date_from": date_from,
                "date_to": date_to,
            })

    def _create_direct_debit_in_payment_mode(self):
        self.ensure_one()
        self = self.sudo()
        payment_mode = self.env["account.payment.mode"].search([
            ("name", "=", "Direct debit"),
            ("company_id", "=", self.id),
        ], limit=1)
        if payment_mode:
            return
        payment_method = self.env["account.payment.method"].search([
            ("code", "=", "sepa_direct_debit"),
        ], limit=1)
        bank_journal = self.env["account.journal"].search([
            ("type", "=", "bank"),
            ("company_id", "=", self.id),
        ], limit=1)
        refund_payment_mode = self.env["account.payment.mode"].search([
            ("name", "=", "Manual"),
            ("company_id", "=", self.id),
        ], limit=1)
        if payment_method:
            self.env["account.payment.mode"].create({
                "name": "Direct debit",
                "company_id": self.id,
                "payment_method_id": payment_method.id,
                "variable_journal_ids": bank_journal,
                "bank_account_link": "variable",
                "refund_payment_mode_id": refund_payment_mode.id,
            })
