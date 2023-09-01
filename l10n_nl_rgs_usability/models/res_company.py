from odoo import api, models
from odoo import SUPERUSER_ID


class Company(models.Model):
    _inherit = "res.company"

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
