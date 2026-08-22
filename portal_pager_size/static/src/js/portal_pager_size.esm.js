/** @odoo-module **/
/* Copyright (C) 2026 XXP
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import publicWidget from "web.public.widget";

publicWidget.registry.PortalPagerSize = publicWidget.Widget.extend({
    selector: ".o_portal_pager_size",
    events: {
        change: "_onChangeSize",
    },

    /**
     * Propagate the current limit to the pager page links: they are built
     * server side by the core `pager()` helper which does not know about
     * the `limit` query parameter.
     *
     * Searchbar links (sort/filter/group/search) already keep it through
     * `keep_query('*')`, so only pager links need to be rewritten.
     *
     * @override
     */
    start() {
        const limit = new URLSearchParams(window.location.search).get("limit");
        if (limit) {
            document
                .querySelectorAll(".o_portal_pager .pagination a.page-link[href]")
                .forEach((link) => {
                    const url = new URL(
                        link.getAttribute("href"),
                        window.location.origin
                    );
                    url.searchParams.set("limit", limit);
                    link.setAttribute("href", url.pathname + url.search + url.hash);
                });
        }
        return this._super(...arguments);
    },

    /**
     * Apply the selected page size: drop the `/page/N` suffix to go back to
     * the first page, keep every other query parameter.
     *
     * @private
     * @param {Event} ev
     */
    _onChangeSize(ev) {
        const url = new URL(window.location.href);
        url.pathname = url.pathname.replace(/\/page\/\d+/, "");
        url.searchParams.set("limit", ev.currentTarget.value);
        window.location.assign(url.href);
    },
});

export default publicWidget.registry.PortalPagerSize;
