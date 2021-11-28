from odoo import models

from odoo.addons.website.models.ir_qweb import AssetsBundleMultiWebsite


class AssetsBundleCriticalCSS(AssetsBundleMultiWebsite):
    def to_node(
        self,
        css=True,
        js=True,
        debug=False,
        async_load=False,
        defer_load=False,
        lazy_load=False,
    ):
        response = super(AssetsBundleCriticalCSS, self).to_node(
            css=css,
            js=js,
            debug=debug,
            async_load=async_load,
            defer_load=defer_load,
            lazy_load=lazy_load,
        )
        if not (css and defer_load):
            return response
        new_response = []
        for item in response:
            if not (item and item[0] == "link"):
                new_response.append(item)
            else:
                attr = item[1]
                attr["media"] = "print"
                attr["onload"] = "this.media='all'"
                new_response.append(("link", attr, None))
        return new_response


class IrQWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    def get_asset_bundle(self, xmlid, files, env=None):
        return AssetsBundleCriticalCSS(xmlid, files, env=env)

    def _get_asset_nodes(
        self,
        xmlid,
        options,
        css=True,
        js=True,
        debug=False,
        async_load=False,
        defer_load=False,
        lazy_load=False,
        values=None,
    ):
        has_critical_css = bool(
            css
            and isinstance(values, dict)
            and values.get("main_object")
            and values["main_object"]._name == "website.page"
            and values["main_object"].critical_css
            and not self.env.user.has_group("website.group_website_designer")
        )
        # toggle defer_load to True in case of css=True and has_critical_css.
        # In core, defer_load is only in use for JS currently,
        # so we can use it for CSS in order to bust tools.ormcache cache, instead
        # of trying to override the tools.ormcache dependency.
        return super(IrQWeb, self)._get_asset_nodes(
            xmlid,
            options,
            css=css,
            js=js,
            debug=debug,
            async_load=async_load,
            defer_load=defer_load or has_critical_css,
            lazy_load=lazy_load,
            values=values,
        )
