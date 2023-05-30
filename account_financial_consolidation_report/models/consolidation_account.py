# © 2011 Guewen Baconnier (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).-
from odoo import fields, models


class ConsolidationAccount(models.Model):
    _inherit = "consolidation.account"

    centralized = fields.Boolean(
        help="If flagged, no details will be displayed in "
        "the General Ledger report (the webkit one only), "
        "only centralized amounts per period.",
    )

    # TODO: Remove all following when André introduces them properly
    user_type_id = fields.Many2one('account.account.type', string='Type', required=True)
    internal_type = fields.Selection(related='user_type_id.type', string="Internal Type", store=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', help="Forces all moves for this account to have this account currency.", tracking=True)
