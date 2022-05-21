odoo.define("website_menu_icon.menu_entry_dialog", function(require) {
    "use strict";

    var contentMenu = require("website.contentMenu");
    var MediaDialog = require("wysiwyg.widgets.MediaDialog");
    var Dialog = require("web.Dialog");
    var core = require("web.core");

    contentMenu.MenuEntryDialog.include({
        template: "website.contentMenu.entry.dialog",
        xmlDependencies: (
            contentMenu.MenuEntryDialog.prototype.xmlDependencies || []
        ).concat(["/website_menu_icon/static/src/xml/website.contentMenu.xml"]),
        events: _.extend({}, contentMenu.MenuEntryDialog.prototype.events, {
            "click i.fa-search": "_onSearchButtonClick",
            "click i.fa-trash": "_onRemoveButtonClick",
        }),

        /**
         * @class
         */
        init: function(parent, options, editable, data) {
            this._super(
                parent,
                _.extend({}, options || {}),
                editable,
                _.extend(
                    {
                        icon: data.icon,
                        icon_type: data.icon_type,
                    },
                    data || {}
                )
            );
        },

        /**
         * @override
         */
        start: function() {
            // Rename the is_new_window checkbox to prevent its removal
            var isNewWindowElement = this.$('input[name="is_new_window"]')[0];
            isNewWindowElement.name = "protect_is_new_window";
            this._super.apply(this, arguments);
            // Rename it back
            isNewWindowElement.name = "is_new_window";
        },

        /**
         * Get the link's data (url, label and styles).
         *
         * @private
         * @returns {Object} {label: String, url: String, classes: String, isNewWindow: Boolean, icon_type: String, icon: String}
         */
        _getData: function() {
            var icon = this.$('input[name="icon"]').val();
            var icon_type = this.$('input[name="icon_type"]').val();
            var result = this._super.apply(this, arguments);
            if (result) {
                result.icon = icon;
                result.icon_type = icon_type;
            }
            return result;
        },

        _onSearchButtonClick: function() {
            var mediaDialog = new MediaDialog(this, {
                noDocuments: true,
                noIcons: false,
                noVideos: true,
            });
            mediaDialog.on("save", this, result => {
                var targetValueObj = this.$el.find("#o_icon_dialog_label_input_value");
                var targetTypeObj = this.$el.find("#o_icon_dialog_label_input_type");
                if (result instanceof HTMLSpanElement) {
                    targetValueObj.val(result.className);
                    targetTypeObj.val("icon");
                } else if (result instanceof HTMLImageElement) {
                    targetValueObj.val(result.attributes.getNamedItem("src").value);
                    targetTypeObj.val("image");
                } else {
                    targetValueObj.val("Unexpected return element");
                    targetTypeObj.val("none");
                }
                // Redraw thew preview icon
                this.$el.find("#o_icon_dialog_label_icon_preview").replaceWith(
                    core.qweb.render("website.contentMenu.entry.dialog.renderIcon", {
                        icon: targetValueObj.val(),
                        icon_type: targetTypeObj.val(),
                    })
                );
            });
            mediaDialog.open();
        },

        _onRemoveButtonClick: function() {
            this.$el.find("#o_icon_dialog_label_input_value").val("");
            this.$el.find("#o_icon_dialog_label_input_type").val("none");
            // Redraw thew preview icon
            this.$el.find("#o_icon_dialog_label_icon_preview").replaceWith(
                core.qweb.render("website.contentMenu.entry.dialog.renderIcon", {
                    icon: "",
                    icon_type: "none",
                })
            );
        },
    });

    contentMenu.EditMenuDialog.include({
        template: "website.contentMenu.dialog.edit",
        xmlDependencies: (
            contentMenu.MenuEntryDialog.prototype.xmlDependencies || []
        ).concat(["/website_menu_icon/static/src/xml/website.contentMenu.xml"]),

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * Called when the "add menu" button is clicked -> Opens the appropriate
         * dialog to edit this new menu.
         *
         * @private
         * @param {Event} ev
         */
        _onAddMenuButtonClick: function(ev) {
            var menuType = ev.currentTarget.dataset.type;
            var dialog = new contentMenu.MenuEntryDialog(this, {}, null, {
                menuType: menuType,
            });
            dialog.on("save", this, link => {
                // Hack to get added values - super's _getData() triggers save before we have chance
                // to add the image and image_type values into result, so we use data structure
                var data = dialog._getData();
                var newMenu = {
                    fields: {
                        id: _.uniqueId("new-"),
                        name: link.text,
                        url: link.url,
                        new_window: link.isNewWindow,
                        is_mega_menu: menuType === "mega",
                        sequence: 0,
                        parent_id: false,
                        icon: data.icon,
                        icon_type: data.icon_type,
                    },
                    children: [],
                    is_homepage: false,
                };
                this.flat[newMenu.fields.id] = newMenu;
                this.$(".oe_menu_editor").append(
                    core.qweb.render("website.contentMenu.dialog.submenu", {
                        submenu: newMenu,
                    })
                );
            });
            dialog.open();
        },
        /**
         * Called when the "edit menu" button is clicked -> Opens the appropriate
         * dialog to edit this menu.
         *
         * @private
         */
        _onEditMenuButtonClick: function(ev) {
            var $menu = $(ev.currentTarget).closest("[data-menu-id]");
            var menuID = $menu.data("menu-id");
            var menu = this.flat[menuID];
            if (menu) {
                var dialog = new contentMenu.MenuEntryDialog(
                    this,
                    {},
                    null,
                    _.extend(
                        {
                            menuType: menu.fields.is_mega_menu ? "mega" : undefined,
                        },
                        menu.fields
                    )
                );
                dialog.on("save", this, link => {
                    // Hack to get added values - save chain prevents inserting it in save method
                    var data = dialog._getData();
                    _.extend(menu.fields, {
                        name: link.text,
                        url: link.url,
                        new_window: data.isNewWindow,
                        icon: data.icon,
                        icon_type: data.icon_type,
                    });
                    // Re-render the menu to show new name and icon
                    $menu.replaceWith(
                        core.qweb.render("website.contentMenu.dialog.submenu", {
                            submenu: menu,
                        })
                    );
                });
                dialog.open();
            } else {
                Dialog.alert(null, "Could not find menu entry");
            }
        },
    });
});
