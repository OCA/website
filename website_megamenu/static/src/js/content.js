// Copyright 2020 Odoo
// Copyright 2020 Tecnativa - Alexandre Díaz
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
odoo.define("website_megamenu.ContentMenu", function (require) {
    "use strict";

    var core = require("web.core");
    var ContentMenu = require("website.contentMenu");

    var qweb = core.qweb;

    ContentMenu.MenuEntryDialog.include({
        xmlDependencies: ContentMenu.MenuEntryDialog.prototype.xmlDependencies.concat([
            "/website_megamenu/static/src/xml/website.contentMenu.xml",
        ]),

        init: function (parent, options, editor, data) {
            this._super.apply(this, arguments);
            this.menuType = data.menuType;
        },

        start: function () {
            // Auto add '#' URL and hide the input if for mega menu
            if (this.menuType === "mega") {
                var $url = this.$('input[name="url"]');
                $url.val("#").trigger("change");
                $url.closest(".form-group").addClass("d-none");
            }
            return this._super.apply(this, arguments);
        },
    });

    ContentMenu.EditMenuDialog.include({
        xmlDependencies: ContentMenu.EditMenuDialog.prototype.xmlDependencies.concat([
            "/website_megamenu/static/src/xml/website.contentMenu.xml",
        ]),

        /**
         * Workarround to handle 'mega' menu type.
         * More code is just cloned from parent.
         *
         * @override
         */
        _onAddMenuButtonClick: function (ev) {
            var self = this;
            var menuType = ev.currentTarget.dataset.type;
            if (menuType === "mega") {
                var dialog = new ContentMenu.MenuEntryDialog(this, {}, null, {
                    menuType: menuType,
                });
                dialog.on("save", this, function (link) {
                    var newMenu = {
                        id: _.uniqueId("new-"),
                        name: link.text,
                        url: link.url,
                        new_window: link.isNewWindow,
                        is_mega_menu: menuType === "mega",
                        sequence: 0,
                        parent_id: false,
                        children: [],
                    };
                    self.flat[newMenu.id] = newMenu;
                    self.$(".oe_menu_editor").append(
                        qweb.render("website.contentMenu.dialog.submenu", {
                            submenu: newMenu,
                        })
                    );
                });
                dialog.open();
            } else {
                this._super.apply(this, arguments);
            }
        },

        /**
         * @override
         */
        start: function () {
            var res = this._super.apply(this, arguments);
            this.$(".oe_menu_editor").nestedSortable({
                listType: "ul",
                handle: "div",
                items: "li",
                maxLevels: 2,
                toleranceElement: "> div",
                forcePlaceholderSize: true,
                opacity: 0.6,
                placeholder: "oe_menu_placeholder",
                tolerance: "pointer",
                attribute: "data-menu-id",
                expression: "()(.+)",
                isAllowed: function (placeholder, placeholderParent, currentItem) {
                    return (
                        !placeholderParent ||
                        (!currentItem[0].dataset.megaMenu &&
                            !placeholderParent[0].dataset.megaMenu)
                    );
                },
            });
            return res;
        },
    });
});
