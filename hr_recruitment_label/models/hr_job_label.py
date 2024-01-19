# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrJobLabel(models.Model):
    _name = "hr.job.label"

    name = fields.Char(translate=True, required=1)
    colour = fields.Integer()
    _sql_constraints = [
        ("name_uniq", "unique (name)", "Label name already exists!"),
    ]
