odoo.define("website_ab_testing.editor", function(require) {
    "use strict";
    var Dialog = require("web.Dialog");
    var core = require("web.core");
    var qweb = core.qweb;
    var _t = core._t;
    var websiteNavbarData = require("website.navbar");

    var AddVariantDialog = Dialog.extend({
        init: function(parent) {
            var options = {
                title: _t("Enter Name"),
                $content: $(qweb.render("website_ab_testing.AddVariantDialog")),
                buttons: [
                    {
                        text: _t("Confirm"),
                        classes: "btn-primary",
                        click: this.confirmClicked.bind(this),
                    },
                    {
                        text: _t("Cancel"),
                        classes: "btn-default",
                        close: true,
                    },
                ],
            };
            return this._super(parent, options);
        },
        confirmClicked: function() {
            this.trigger("confirm", this.$('input[name="name"]').val());
        },
    });

    var ABTestingMenu = websiteNavbarData.WebsiteNavbarActionWidget.extend({
        events: _.extend(
            {},
            websiteNavbarData.WebsiteNavbarActionWidget.prototype.events || {},
            {
                "click .ab_testing_add": "_onAddVariantClick",
                "click .ab_testing_select": "_onSelectVariantClick",
                "click .ab_testing_delete": "_onDeleteVariantClick",
                "click .ab_testing_toggle": "_onToggleABTestingClick",
            }
        ),

        xmlDependencies: ["/website_ab_testing/static/src/xml/editor.xml"],

        start: function() {
            var res = this._super.apply(this, arguments);
            this.masterId = Number(
                this.$el.find('[data-master-variant="1"]').data("id")
            );
            return res;
        },

        _onAddVariantClick: function() {
            var addDialog = new AddVariantDialog(this);
            addDialog.on(
                "confirm",
                this,
                function(name) {
                    this._createVariant(name)
                        .then(this._switchVariant.bind(this))
                        .then(function() {
                            window.location.reload();
                        });
                    addDialog.close();
                }.bind(this)
            );
            addDialog.open();
        },

        _onDeleteVariantClick: function(ev) {
            var $target = $(ev.target);
            var variantId = Number($target.data("id"));
            this._deleteVariant(variantId).then(function() {
                window.location.reload();
            });
        },

        _onToggleABTestingClick: function(ev) {
            ev.stopImmediatePropagation();
            this._toggleABTesting();
        },

        _onSelectVariantClick: function(ev) {
            var $target = $(ev.target);
            var variantId = Number($target.data("id"));
            this._switchVariant(variantId).then(function() {
                window.location.reload();
            });
        },

        _toggleABTesting: _.debounce(function() {
            return this._rpc({
                model: "ir.ui.view",
                method: "toggle_ab_testing_enabled",
                args: [[this.masterId]],
            });
        }, 100),

        _switchVariant: function(variantId) {
            return this._rpc({
                model: "ir.ui.view",
                method: "switch_variant",
                args: [[this.masterId], variantId],
            });
        },

        _createVariant: function(name) {
            return this._rpc({
                model: "ir.ui.view",
                method: "create_variant",
                args: [[this.masterId], name],
            });
        },

        _deleteVariant: function(variantId) {
            return this._rpc({
                model: "ir.ui.view",
                method: "unlink",
                args: [[variantId]],
            });
        },
    });

    websiteNavbarData.websiteNavbarRegistry.add(ABTestingMenu, "#ab_testing_menu");

    return {
        AddVariantDialog: AddVariantDialog,
        ABTestingMenu: ABTestingMenu,
    };
});
