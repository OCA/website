// Copyright 2020 Odoo
// Copyright 2020 Tecnativa - Alexandre Díaz
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
odoo.define("website_megamenu.EditorMenu", function (require) {
    "use strict";

    var EditorMenuBar = require("web_editor.editor");

    /**
     * Show/hide the dropdowns associated to the given toggles and allows to wait
     * for when it is fully shown/hidden.
     *
     * Note: this also takes care of the fact the 'toggle' method of bootstrap does
     * not properly work in all cases.
     *
     * @param {jQuery} $toggles
     * @param {Boolean} [show]
     * @returns {Promise<jQuery>}
     */
    function toggleDropdown($toggles, show) {
        return Promise.all(
            _.map($toggles, function (toggle) {
                var $toggle = $(toggle);
                var $dropdown = $toggle.parent();
                var shown = $dropdown.hasClass("show");
                if (shown === show) {
                    return;
                }
                var toShow = !shown;
                return new Promise(function (resolve) {
                    $dropdown.one(
                        toShow ? "shown.bs.dropdown" : "hidden.bs.dropdown",
                        function () {
                            return resolve();
                        }
                    );
                    if (toShow) {
                        $toggle.dropdown("toggle");
                        $(".o_mega_menu.show").addClass("show");
                    } else {
                        $(".o_mega_menu.show").removeClass("show");
                        // This version of bootstrap doesn't have a method to 'hide' the dropdown
                        // so the 'hidden.bs.dropdown' is never dispatched. We force it to get all working as expected.
                        $dropdown.removeClass("show").trigger("hidden.bs.dropdown");
                    }
                });
            })
        ).then(function () {
            return $toggles;
        });
    }

    EditorMenuBar.Class.include({
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Mega menu initialization: handle dropdown openings by hand
                var $megaMenuToggles = $(".o_mega_menu_toggle");
                $megaMenuToggles.removeAttr("data-toggle").dropdown("dispose");
                $megaMenuToggles.on("click", function (ev) {
                    var $toggle = $(ev.currentTarget);

                    // Each time we toggle a dropdown, we will destroy the dropdown
                    // behavior afterwards to keep manual control of it
                    var dispose = function ($els) {
                        return $els.dropdown("dispose");
                    };

                    // First hide all other mega menus
                    toggleDropdown($megaMenuToggles.not($toggle), false).then(dispose);

                    // Then toggle the clicked one
                    toggleDropdown($toggle)
                        .then(dispose)
                        .then(function ($els) {
                            var isShown = $els.parent().hasClass("show");
                            self.snippetsMenu.toggleMegaMenuSnippets(isShown);
                        });
                });

                if (self.$(".o_mega_menu").hasClass("show")) {
                    self.snippetsMenu.toggleMegaMenuSnippets(true);
                }
            });
        },

        /**
         * @override
         */
        destroy: function () {
            this.snippetsMenu.toggleMegaMenuSnippets(false);
            this._super.apply(this, arguments);
        },
    });
});
