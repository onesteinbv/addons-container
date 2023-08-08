
from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        chart_template = self.env.company.chart_template_id
        is_rgs = chart_template == self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template')
        is_bank = self.env.context.get('domain_account_journal_type') == "bank"
        prefix = chart_template.bank_account_code_prefix
        if is_rgs and is_bank and prefix and operator == "ilike":
            args = args or []
            args = [("code", "=ilike", prefix + "%")] + args
        return super().name_search(name, args=args, operator=operator, limit=limit)
