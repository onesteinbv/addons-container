# Copyright 2022 Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    font = fields.Selection(
        selection_add=[
            ("Gandhi Serif", "Gandhi Serif"), ("Gandhi Serif Bold", "Gandhi Serif Bold"),
            ("Gandhi Serif Bold Italic", "Gandhi Serif Bold Italic"),("Gandhi Serif Italic", "Gandhi Serif Italic"),
        ]
    )
