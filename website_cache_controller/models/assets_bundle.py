from odoo.addons.base.models.assetsbundle import AssetsBundle

get_asset_template_url = AssetsBundle._get_asset_template_url


def _get_asset_template_url(self):
    """Monkeypatch method to use cacheable path for frontend assets"""
    return get_asset_template_url(self).replace(
        '/web/content', '/website/cache/content'
    )


AssetsBundle._get_asset_template_url = _get_asset_template_url
