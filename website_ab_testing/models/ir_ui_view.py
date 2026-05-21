import random

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.http import request


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    ab_testing_enabled = fields.Boolean(string="A/B Testing", copy=False)

    master_id = fields.Many2one(comodel_name="ir.ui.view", copy=False)

    variant_ids = fields.One2many(
        comodel_name="ir.ui.view", inverse_name="master_id", string="Variants"
    )

    def render(self, values=None, engine="ir.qweb", minimal_qcontext=False):
        website = self.env["website"].get_current_website()
        if (
            request
            and request.session
            and website
            and self.ab_testing_enabled
            and not self.env.user.has_group("website.group_website_publisher")
        ):
            if "ab_testing" not in request.session:
                request.session["ab_testing"] = {"active_variants": {}}
            if self.id not in request.session["ab_testing"]["active_variants"]:
                random_index = random.randint(0, len(self.variant_ids))
                selected_view = self
                if random_index:
                    selected_view = self.variant_ids[random_index - 1]
                ab_testing = request.session["ab_testing"].copy()
                ab_testing["active_variants"][self.id] = selected_view.id
                request.session["ab_testing"] = ab_testing
                return selected_view.render(values, engine, minimal_qcontext)
            else:
                selection_view_id = request.session["ab_testing"]["active_variants"][
                    self.id
                ]
                if selection_view_id == self.id:
                    return super().render(values, engine, minimal_qcontext)
                selected_view = self.search([("id", "=", selection_view_id)])
                if selected_view:
                    return selected_view.render(values, engine, minimal_qcontext)
                ab_testing = request.session["ab_testing"].copy()
                del ab_testing["active_variants"][self.id]
        elif (
            request
            and request.session
            and website
            and self.env.user.has_group("website.group_website_publisher")
        ):
            variants = self.env["ir.ui.view"]
            if self.master_id:
                variants += self.master_id
                variants += self.master_id.variant_ids
            else:
                variants += self
                variants += self.variant_ids
            if values is None:
                values = {}
            values["ab_testing_variants"] = variants

            if (
                "ab_testing" in request.session
                and not self.master_id
                and self.id in request.session["ab_testing"]["active_variants"]
            ):
                active_variant = self.variant_ids.filtered(
                    lambda v: v.id
                    == request.session["ab_testing"]["active_variants"][self.id]
                )
                if active_variant:
                    values["active_variant"] = active_variant
                    return active_variant.render(values, engine, minimal_qcontext)

        return super().render(values, engine, minimal_qcontext)

    def create_variant(self, name):
        self.ensure_one()
        if self.master_id:
            raise UserError(_("Cannot create variant of variant."))
        if self.variant_ids.filtered(lambda v: v.name == name):
            raise UserError(_("Variant '%s' already exists.") % name)
        variant = self.copy({"name": name, "master_id": self.id})
        self._copy_inheritance(variant.id)
        return variant.id

    def _copy_inheritance(self, new_id):
        """Copy the inheritance recursively"""
        for view in self:
            for child in view.inherit_children_ids:
                copy = child.copy({"inherit_id": new_id})
                child._copy_inheritance(copy.id)

    def toggle_ab_testing_enabled(self):
        self.ensure_one()
        if self.master_id:
            raise UserError(_("This is not the master page."))
        self.ab_testing_enabled = not self.ab_testing_enabled

    def switch_variant(self, variant_id):
        self.ensure_one()
        if not self.env.user.has_group("website.group_website_publisher"):
            raise AccessError(
                _("Cannot deliberately switch variant as non-designer user.")
            )
        if not variant_id:
            raise UserError(_("No variant specified."))

        if "ab_testing" not in request.session:
            request.session["ab_testing"] = {"active_variants": {}}
        ab_testing = request.session["ab_testing"].copy()
        ab_testing["active_variants"][self.id] = variant_id
        request.session["ab_testing"] = ab_testing

    @api.model
    def get_active_variants(self):
        if "ab_testing" not in request.session:
            request.session["ab_testing"] = {"active_variants": {}}
        ids = list(request.session["ab_testing"]["active_variants"].values())
        return self.search([("id", "in", ids)])
