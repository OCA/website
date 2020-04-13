# Copyright 2020 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from copy import deepcopy
from xml.sax.saxutils import escape

from lxml import etree as ElementTree

from odoo import SUPERUSER_ID, api


def _merge_views(env, xmlids):
    old_view_ids = env["ir.ui.view"].search(
        [("key", "in", xmlids), ("active", "=", True)]
    )
    # Get only the edited version of the views (if has it)
    old_view_ids_edited = old_view_ids.filtered("website_id")
    old_view_ids_edited_keys = old_view_ids_edited.mapped("key")
    views_to_discard = env["ir.ui.view"]
    for old_view in old_view_ids:
        if not old_view.website_id and old_view.key in old_view_ids_edited_keys:
            views_to_discard |= old_view
    old_view_ids -= views_to_discard
    new_website_page = env.ref("website_legal_page.legal_page_page")
    new_view_id = env.ref("website_legal_page.legal_page")
    # 'Dolly' separator element
    separator = ElementTree.fromstring(
        "<div class='s_hr text-left pt32 pb32' data-name='Separator'>"
        + "<hr class='s_hr_1px s_hr_solid border-600 w-100 mx-auto'/></div>"
    )
    # Replace new content with the old one per website
    website_ids = old_view_ids.mapped("website_id")
    for website_id in website_ids:
        new_xml = ElementTree.fromstring(new_view_id.arch)
        table_content_list = new_xml.xpath("//div[@id='section_list']/ul")[0]
        sections_content = new_xml.xpath("//div[@id='section_content']")[0]
        has_views_edited = any(
            old_view_ids_edited.filtered(lambda x: x.website_id == website_id)
        )
        # Remove 'IS A SAMPLE' alert
        if has_views_edited:
            alert = new_xml.xpath(
                "//section[@data-name='Title']//div[@data-name='Alert']"
            )[0]
            alert.find("..").remove(alert)
        # Remove unused content
        for child in table_content_list.getchildren():
            table_content_list.remove(child)
        for child in sections_content.getchildren():
            sections_content.remove(child)
        views_done = env["ir.ui.view"]
        for old_view_id in old_view_ids:
            if old_view_id.website_id != website_id:
                continue
            anchor_name = old_view_id.key.split(".")[1]
            # Insert item in table content list
            list_item = ElementTree.fromstring(
                "<li><p><a href='#{}'>{}</a></p></li>".format(
                    anchor_name, escape(old_view_id.name)
                )
            )
            table_content_list.append(list_item)
            # Insert section content
            old_xml = ElementTree.fromstring(old_view_id.arch)
            old_content = old_xml.xpath("//div[@id='wrap']")[0]
            sections_content.append(deepcopy(separator))
            sections_content.append(
                ElementTree.fromstring(
                    "<a class='legal_anchor' id='%s'/>" % anchor_name
                )
            )
            for children in old_content.getchildren():
                sections_content.append(children)
            views_done |= old_view_id
        old_view_ids -= views_done
        # Create a new page with the changes
        view_id = env["ir.ui.view"].create(
            {
                "arch": ElementTree.tostring(new_xml, encoding="unicode"),
                "website_id": website_id.id,
                "key": new_view_id.key,
                "name": new_view_id.name,
                "type": "qweb",
            }
        )
        env["website.page"].create(
            {
                "name": new_website_page.name,
                "url": new_website_page.url,
                "view_id": view_id.id,
                "is_published": True,
                "website_id": website_id.id,
                "website_indexed": True,
                "website_published": True,
            }
        )


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        is_website_sale_installed = (
            env["ir.module.module"].search_count(
                [("name", "=", "website_sale"), ("state", "=", "installed")]
            )
            > 0
        )
        if is_website_sale_installed:
            _merge_views(env, ["website_sale.terms"])
