
from odoo import api, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.depends('type', 'currency_id')
    def _compute_outbound_payment_method_line_ids(self):
        res = super()._compute_outbound_payment_method_line_ids()
        self._set_journal_bank_payment_credit_account()
        return res

    def _set_journal_bank_payment_credit_account(self):
        for journal in self.filtered(lambda j: j.type == "bank"):
            if journal.company_id.chart_template_id == self.env.ref('l10n_nl_rgs.l10nnl_rgs_chart_template', False):
                lines = journal.outbound_payment_method_line_ids
                sepa_lines = lines.filtered(lambda l: l.payment_method_id.code == "sepa_credit_transfer")
                for line in sepa_lines:
                    line.payment_account_id = journal.company_id.account_journal_payment_credit_account_id
