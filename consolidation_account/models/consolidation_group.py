# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ConsolidationGroup(models.Model):
    _name = "consolidation.group"
    _description = "Consolidation Group"
    _parent_store = True
    _order = "code_prefix_start"

    parent_id = fields.Many2one(
        "consolidation.group", index=True, ondelete="cascade", readonly=True
    )
    parent_path = fields.Char(index=True, unaccent=False)
    name = fields.Char(required=True, translate=True)
    code_prefix_start = fields.Char()
    code_prefix_end = fields.Char()
    chart_id = fields.Many2one("consolidation.chart", required=True)

    account_ids = fields.One2many(
        comodel_name="consolidation.account",
        inverse_name="group_id",
        string="Accounts",
    )

    _sql_constraints = [
        (
            "check_length_prefix",
            "CHECK(char_length(COALESCE(code_prefix_start, '')) = char_length(COALESCE(code_prefix_end, '')))",
            "The length of the starting and the ending code prefix must be the same",
        ),
    ]

    @api.onchange("code_prefix_start")
    def _onchange_code_prefix_start(self):
        if not self.code_prefix_end or self.code_prefix_end < self.code_prefix_start:
            self.code_prefix_end = self.code_prefix_start

    @api.onchange("code_prefix_end")
    def _onchange_code_prefix_end(self):
        if not self.code_prefix_start or self.code_prefix_start > self.code_prefix_end:
            self.code_prefix_start = self.code_prefix_end

    def name_get(self):
        result = []
        for group in self:
            prefix = group.code_prefix_start and str(group.code_prefix_start)
            if prefix and group.code_prefix_end != group.code_prefix_start:
                prefix += "-" + str(group.code_prefix_end)
            name = (prefix and (prefix + " ") or "") + group.name
            result.append((group.id, name))
        return result

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        if operator == "ilike" and not (name or "").strip():
            domain = []
        else:
            criteria_operator = (
                ["|"]
                if operator not in expression.NEGATIVE_TERM_OPERATORS
                else ["&", "!"]
            )
            domain = criteria_operator + [
                ("code_prefix_start", "=ilike", name + "%"),
                ("name", operator, name),
            ]
        return self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )

    @api.constrains("code_prefix_start", "code_prefix_end")
    def _constraint_prefix_overlap(self):
        self.env["consolidation.group"].flush()
        query = """
            SELECT other.id FROM consolidation_group this
            JOIN consolidation_group other
              ON char_length(other.code_prefix_start) = char_length(this.code_prefix_start)
             AND other.id != this.id
             AND other.chart_id = this.chart_id
             AND (
                other.code_prefix_start <= this.code_prefix_start AND this.code_prefix_start <= other.code_prefix_end
                OR
                other.code_prefix_start >= this.code_prefix_start AND this.code_prefix_end >= other.code_prefix_start
            )
            WHERE this.id IN %(ids)s
        """
        self.env.cr.execute(query, {"ids": tuple(self.ids)})
        res = self.env.cr.fetchall()
        if res:
            raise ValidationError(
                _("Consolidation Groups with the same granularity can't overlap")
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "code_prefix_start" in vals and not vals.get("code_prefix_end"):
                vals["code_prefix_end"] = vals["code_prefix_start"]
        res_ids = super(ConsolidationGroup, self).create(vals_list)
        res_ids._adapt_accounts_for_consolidation_groups()
        res_ids._adapt_parent_consolidation_group()
        return res_ids

    def write(self, vals):
        res = super(ConsolidationGroup, self).write(vals)
        if "code_prefix_start" in vals or "code_prefix_end" in vals:
            self._adapt_accounts_for_consolidation_groups()
            self._adapt_parent_consolidation_group()
        return res

    def unlink(self):
        for record in self:
            account_ids = self.env["consolidation.account"].search(
                [("group_id", "=", record.id)]
            )
            account_ids.write({"group_id": record.parent_id.id})

            children_ids = self.env["consolidation.group"].search(
                [("parent_id", "=", record.id)]
            )
            children_ids.write({"parent_id": record.parent_id.id})
        super(ConsolidationGroup, self).unlink()

    def _adapt_accounts_for_consolidation_groups(self, account_ids=None):
        """Ensure consistency between accounts and consolidation groups.

        Find and set the most specific group matching the code of the account.
        The most specific is the one with the longest prefixes and with the starting
        prefix being smaller than the account code and the ending prefix being greater.
        """
        chart_ids = account_ids.chart_id.ids if account_ids else self.chart_id.ids
        account_ids = account_ids.ids if account_ids else []
        if not chart_ids and not account_ids:
            return
        self.env["consolidation.group"].flush(self.env["consolidation.group"]._fields)
        self.env["consolidation.account"].flush(
            self.env["consolidation.account"]._fields
        )

        account_where_clause = ""
        where_params = [tuple(chart_ids)]
        if account_ids:
            account_where_clause = "AND account.id IN %s"
            where_params.append(tuple(account_ids))

        self._cr.execute(
            f"""
            WITH candidates_account_groups AS (
                SELECT
                    account.id AS account_id,
                    ARRAY_AGG(agroup.id ORDER BY char_length(agroup.code_prefix_start) DESC, agroup.id) AS group_ids
                FROM consolidation_account account
                LEFT JOIN consolidation_group agroup
                    ON agroup.code_prefix_start <= LEFT(account.code, char_length(agroup.code_prefix_start))
                    AND agroup.code_prefix_end >= LEFT(account.code, char_length(agroup.code_prefix_end))
                    AND agroup.chart_id = account.chart_id
                WHERE account.chart_id IN %s {account_where_clause}
                GROUP BY account.id
            )
            UPDATE consolidation_account
            SET group_id = rel.group_ids[1]
            FROM candidates_account_groups rel
            WHERE consolidation_account.id = rel.account_id
        """,
            where_params,
        )
        self.env["consolidation.account"].invalidate_cache(fnames=["group_id"])

    def _adapt_parent_consolidation_group(self):
        """Ensure consistency of the hierarchy of consolidation groups.

        Find and set the most specific parent for each group.
        The most specific is the one with the longest prefixes and with the starting
        prefix being smaller than the child prefixes and the ending prefix being greater.
        """
        if not self:
            return
        self.env["consolidation.group"].flush(self.env["consolidation.group"]._fields)
        query = """
            WITH relation AS (
       SELECT DISTINCT FIRST_VALUE(parent.id) OVER (PARTITION BY child.id ORDER BY child.id, char_length(parent.code_prefix_start) DESC) AS parent_id,
                       child.id AS child_id
                  FROM consolidation_group parent
                  JOIN consolidation_group child
                    ON char_length(parent.code_prefix_start) < char_length(child.code_prefix_start)
                   AND parent.code_prefix_start <= LEFT(child.code_prefix_start, char_length(parent.code_prefix_start))
                   AND parent.code_prefix_end >= LEFT(child.code_prefix_end, char_length(parent.code_prefix_end))
                   AND parent.id != child.id
                   AND parent.chart_id = child.chart_id
                 WHERE child.chart_id IN %(chart_ids)s
            )
            UPDATE consolidation_group child
               SET parent_id = relation.parent_id
              FROM relation
             WHERE child.id = relation.child_id;
        """
        self.env.cr.execute(query, {"chart_ids": tuple(self.chart_id.ids)})
        self.env["consolidation.group"].invalidate_cache(fnames=["parent_id"])
        self.env["consolidation.group"].search(
            [("chart_id", "in", self.chart_id.ids)]
        )._parent_store_update()
