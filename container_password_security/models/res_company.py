# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    password_special = fields.Integer(
        default=0,
    )
    password_minimum = fields.Integer(
        default=0
    )
    password_history = fields.Integer(
        default=0
    )
