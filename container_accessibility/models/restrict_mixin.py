from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class RestrictMixin(models.AbstractModel):
    _name = "container.restrict.mixin"
    _description = "Restrict Mixin"

    @api.model
    def _get_restrict_domain(self):
        return None

    def _check_restrict(self):
        if (
            not self.env.user.is_restricted_user() or
            self.env.context.get("no_restrict", False) or
            self.env.su
        ):
            return
        restrict_domain = self._get_restrict_domain()
        if restrict_domain is None or not self.filtered_domain(restrict_domain):
            raise AccessError(_("Access denied to this model (%s)", self._name))

    def write(self, vals):
        self._check_restrict()
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        self._check_restrict()
        return super().create(vals_list)

    def unlink(self):
        self._check_restrict()
        return super().unlink()


class ResGroups(models.Model):
    _name = "res.groups"
    _inherit = ["res.groups", "container.restrict.mixin"]


class ActionsActions(models.Model):
    _name = "ir.actions.actions"
    _inherit = ["ir.actions.actions", "container.restrict.mixin"]


class IrCron(models.Model):
    _name = "ir.cron"
    _inherit = ["ir.cron", "container.restrict.mixin"]


class IrCronTrigger(models.Model):
    _name = "ir.cron.trigger"
    _inherit = ["ir.cron.trigger", "container.restrict.mixin"]


class DecimalPrecision(models.Model):
    _name = "decimal.precision"
    _inherit = ["decimal.precision", "container.restrict.mixin"]


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = ["ir.model", "container.restrict.mixin"]


class IrModelFields(models.Model):
    _name = "ir.model.fields"
    _inherit = ["ir.model.fields", "container.restrict.mixin"]


class IrModelFieldsSelection(models.Model):
    _name = "ir.model.fields.selection"
    _inherit = ["ir.model.fields.selection", "container.restrict.mixin"]


class IrModelConstraint(models.Model):
    _name = "ir.model.constraint"
    _inherit = ["ir.model.constraint", "container.restrict.mixin"]


class IrModelRelation(models.Model):
    _name = "ir.model.relation"
    _inherit = ["ir.model.relation", "container.restrict.mixin"]


class IrRule(models.Model):
    _name = "ir.rule"
    _inherit = ["ir.rule", "container.restrict.mixin"]


class IrModelAccess(models.Model):
    _name = "ir.model.access"
    _inherit = ["ir.model.access", "container.restrict.mixin"]


class IrUIMenu(models.Model):
    _name = "ir.ui.menu"
    _inherit = ["ir.ui.menu", "container.restrict.mixin"]


class WebTour(models.Model):
    _name = "web_tour.tour"
    _inherit = ["web_tour.tour", "container.restrict.mixin"]


class PaperFormat(models.Model):
    _name = "report.paperformat"
    _inherit = ["report.paperformat", "container.restrict.mixin"]


class IrUiView(models.Model):
    _name = "ir.ui.view"
    _inherit = ["ir.ui.view", "container.restrict.mixin"]

    @api.model
    def _get_restrict_domain(self):
        return [("type", "=", "qweb")]
