# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ConsolidationAccount(models.Model):
    _name = "consolidation.account"
    _description = "Consolidation account"

    _sql_constraints = [
        (
            "code_chart_uniq",
            "unique (code, chart_id)",
            "The code of the account must be unique !",
        )
    ]

    def _get_default_chart(self):
        return self.env["consolidation.chart"].search([], limit=1)

    name = fields.Char(required=True, index=True)
    chart_id = fields.Many2one(
        comodel_name="consolidation.chart",
        string="Consolidation Chart",
        ondelete="cascade",
        required=True,
        default=_get_default_chart,
    )
    code = fields.Char(required=True, index=True)
    deprecated = fields.Boolean(index=True)

    account_ids = fields.Many2many(
        comodel_name="account.account",
        relation="account_consolidation_account_rel",
        column1="consolidation_account_id",
        column2="account_id",
        string="Accounts",
    )
    group_id = fields.Many2one(comodel_name="consolidation.group")
    tag_ids = fields.Many2many(
        comodel_name="account.account.tag",
        relation="consolidation_account_account_tag",
        column1="consolidation_account_id",
        column2="account_tag_id",
        domain=[("applicability", "=", "accounts")],
        string="Tags",
        help="Optional tags you may want to assign for custom reporting",
    )

    def _compute_account_ids(self):
        for rec in self:
            rec.account_ids = self.env["account.account"].search(
                [("consolidation_account_ids", "in", [rec.id])]
            )

    # @api.model
    # def _name_search(
    #     self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    # ):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = [
    #             "|",
    #             ("code", "=ilike", name.split(" ")[0] + "%"),
    #             ("name", operator, name),
    #         ]
    #         if operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = ["&", "!"] + domain[1:]
    #     account_ids = self._search(
    #         expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
    #     )
    #     return models.lazy_name_get(self.browse(account_ids).with_user(name_get_uid))

    # def name_get(self):
    #     result = []
    #     for account in self:
    #         name = account.code + " " + account.name
    #         result.append((account.id, name))
    #     return result
