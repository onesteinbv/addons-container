# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrJob(models.Model):
    _inherit = "hr.job"

    label_ids = fields.Many2many(comodel_name="hr.job.label")
