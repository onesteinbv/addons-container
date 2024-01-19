from lxml import etree

from odoo import Command, api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_multi_company_groups(self):
        return ["base.group_multi_company"]

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form":
            multi_company_groups = self._get_multi_company_groups()
            for group in multi_company_groups:
                erp_group_id = self.env.ref(group).id
                sel_xpath = (
                    "//field[contains(@name, 'sel_groups_%s_')]/.." % erp_group_id
                )
                in_xpath = "//field[@name='in_group_%s']" % erp_group_id
                xml = etree.XML(res["arch"])
                xml_groups = xml.xpath(sel_xpath) + xml.xpath(in_xpath)
                for xml_group in xml_groups:
                    xml_group.getparent().remove(xml_group)
                res["arch"] = etree.tostring(xml, encoding="unicode")
        return res

    def _force_multi_company_groups(self):
        multi_company_groups = self._get_multi_company_groups()
        for user in self.filtered(lambda u: u._is_internal()):
            for group in multi_company_groups:
                if not user.has_group(group):
                    continue
                group_record = self.env.ref(group)
                user.sudo().with_context(no_multi_company_group_force=True).write(
                    {"groups_id": [Command.unlink(group_record.id)]}
                )

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("no_multi_company_group_force"):
            self._force_multi_company_groups()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.context.get("no_multi_company_group_force"):
            res._force_multi_company_groups()
        return res
