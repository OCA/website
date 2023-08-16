from odoo import models

from odoo.addons.website.models.ir_qweb import AssetsBundleMultiWebsite


class AssetsBundleCriticalCSS(AssetsBundleMultiWebsite):
    def to_node(
        self,
        css=True,
        js=True,
        debug=False,
        async_load=False,
    ):
        response = super(AssetsBundleCriticalCSS, self).to_node(
            css=css,
            js=js,
            debug=debug,
            async_load=async_load,
        )
        if not (css):
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
