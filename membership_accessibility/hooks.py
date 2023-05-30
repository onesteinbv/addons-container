# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    user_group_id = env['ir.model.data']._xmlid_to_res_id('base.group_user')
    existing_internal_non_member_users = env["res.users"].search(
        [('partner_id.membership_state', '=', 'none'), ('groups_id', 'in', [user_group_id])])
    sale_crm_contacts_access_group = env.ref('membership_accessibility.group_sale_crm_contact_access')
    existing_internal_non_member_users.write({'groups_id': [(4, sale_crm_contacts_access_group.id)]})


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    crm_menu = env.ref('crm.crm_menu_root')
    crm_menu.write({'groups_id': [
        (6, 0, [env.ref('sales_team.group_sale_salesman').id, env.ref('sales_team.group_sale_manager').id])]})
    contacts_menu = env.ref('contacts.menu_contacts')
    contacts_menu.write({'groups_id': [
        (6, 0, [env.ref('base.group_user').id, env.ref('base.group_partner_manager').id])]})
