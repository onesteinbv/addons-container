from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env['res.company'].sudo().search([]):
        company.write({'currency_rates_autoupdate': False})

    for journal in env['account.journal'].sudo().search([('type', '=', 'sale')]):
        journal.write({'check_chronology': True})
    for journal in env['account.journal'].sudo().search([('type', '=', 'purchase')]):
        journal.write({'check_chronology': False})
