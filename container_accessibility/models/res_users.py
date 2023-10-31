from lxml import etree
from odoo import api, fields, models, Command


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_forced_groups(self):
        return ["container_accessibility.group_curq"]

    def is_allowed_overriding_forced_groups(self):
        self.ensure_one()
        return (
            self.env.ref("base.user_admin") == self or
            self.env.ref("base.user_root") == self
        )

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        allow_override = self.env.user.is_allowed_overriding_forced_groups()
        if view_type == "form" and not allow_override:
            forced_groups = self._get_forced_groups()
            for group in forced_groups:
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

    def _force_groups(self):
        allow_override = self.env.user.is_allowed_overriding_forced_groups()
        if allow_override:
            return
        forced_groups = self._get_forced_groups()
        for user in self:
            for group in forced_groups:
                if user.has_group(group):
                    continue
                group_record = self.env.ref(group)
                user.with_context(no_group_force=True).write({
                    "groups_id": [Command.link(group_record.id)]
                })

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("no_group_force"):
            self._force_groups()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if not self.env.context.get("no_group_force"):
            res._force_groups()
        return res
