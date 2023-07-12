# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})
    companies = env["res.company"].search([])
    companies.write({
        "password_special": 0,
        "password_history": 0
    })
