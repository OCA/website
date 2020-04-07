# Copyright 2020 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from lxml import etree as ElementTree

from odoo import SUPERUSER_ID, api


def _merge_view(env):
    legal_page_view_ids = env["ir.ui.view"].search(
        [("key", "=", "website_legal_page.legal_page"), ("active", "=", True)]
    )
    # Get only the edited version of the views (if has it)
    legal_page_view_ids_edited = legal_page_view_ids.filtered("website_id")
    legal_page_view_ids_edited_keys = legal_page_view_ids_edited.mapped("key")
    views_to_discard = env["ir.ui.view"]
    for legal_page_view in legal_page_view_ids:
        if (
            not legal_page_view.website_id
            and legal_page_view.key in legal_page_view_ids_edited_keys
        ):
            views_to_discard |= legal_page_view

    legal_page_view_ids -= views_to_discard
    to_merge_view_id = env.ref("website_cookie_notice.legal_cookie_policy")
    to_merge_xml = ElementTree.fromstring(to_merge_view_id.arch)
    table_content_list = to_merge_xml.xpath("//div[@id='add_list']")[0]
    sections_content = to_merge_xml.xpath("//div[@id='add_content']")[0]
    # Replace new content with the old one per website
    website_ids = legal_page_view_ids.mapped("website_id")
    for website_id in website_ids.ids + [False]:
        views_done = env["ir.ui.view"]
        for legal_page_view_id in legal_page_view_ids:
            if legal_page_view_id.website_id.id != website_id:
                continue
            # Insert section content
            legal_page_xml = ElementTree.fromstring(legal_page_view_id.arch)
            legal_page_content_list = legal_page_xml.xpath(
                "//div[@id='section_list']/ul"
            )[0]
            legal_page_content = legal_page_xml.xpath("//div[@id='section_content']")[0]
            for children in table_content_list.getchildren():
                legal_page_content_list.append(children)
            for children in sections_content.getchildren():
                legal_page_content.append(children)
            legal_page_view_id.arch = ElementTree.tostring(
                legal_page_xml, encoding="unicode"
            )
            views_done |= legal_page_view_id
        legal_page_view_ids -= views_done


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _merge_view(env)
