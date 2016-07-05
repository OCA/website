/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

"use strict";
odoo.define("website_portal_purchase_product_sale_packaging_price.loader",
            function (require) {

var animation = require("web_editor.snippets.animation");
var core = require("web.core");
var Model = require("web.Model");
var Session = require("web.Session");
var $ = require("$");

animation.registry.website_portal_purchase_product_sale_packaging_price =
animation.Class.extend({
    selector: ".o_my_purchase_product_form" +
              ":has(.js_packaging_placeholder, .js_packaging_add)",
    start: function (editable_mode) {
        if (editable_mode) {
            return $.Deferred().reject();
        }

        this.new_count = 0;
        this.$placeholder = this.$(".js_packaging_placeholder");
        this.$add = this.$(".js_packaging_add");
        this.product_tmpl_id = Number(this.$placeholder.data("product"));
        this.currency = {
            position: this.$placeholder.data("currency-position"),
            symbol: this.$placeholder.data("currency-symbol"),
        };
        this.Packaging = new Model("product.packaging");
        this.Packaging._fields =
            ["id", "name", "list_price", "qty", "package_material_id"];
        this.Packaging._domain =
            [["product_tmpl_id", "=", this.product_tmpl_id]];
        this.PackagingMaterial = new Model("product.packaging.material");
        this.PackagingMaterial._fields = ["id", "display_name"];
        core.qweb.add_template(
            "/website_portal_purchase_product_sale_packaging_price" +
            "/static/src/xml/packaging.xml");
        this.bind_events();
        return this.load_first_run();
    },
    bind_events: function () {
        var this_ = this;
        this.$el.on("click", ".js_packaging_delete", function (event) {
            return this_.delete_packaging(event);
        });
        this.$add.on("click", function (event) {
            return this_.add_packaging_empty(event);
        });
    },
    load_first_run: function () {
        var this_ = this;
        return $.when(
            this.load_materials(),
            this.load_packagings()
        ).done(function (materials, packagings) {
            this_.add_packagings(packagings);
        });
    },
    load_materials: function () {
        var this_ = this;
        return this.PackagingMaterial
        .call("search_read", [[], this.PackagingMaterial._fields])
        .done(function (records) {
            this_.materials = records;
        });
    },
    load_packagings: function () {
        var this_ = this;
        return this.Packaging
        .call("search_read", [this.Packaging._domain, this.Packaging._fields]);
    },
    empty_packaging: function () {
        var result = new Object();
        $.each(this.Packaging._fields, function (index, value) {
            result[value] = null;
        });
        result.id = "new" + this.new_count++;
        result.package_material_id = [];
        return result;
    },
    add_packagings: function (packagings) {
        for (var row in packagings) {
            this.add_packaging(packagings[row]);
        }
    },
    add_packaging: function (packaging) {
        this.$placeholder.append(
            core.qweb.render(
                "website_portal_purchase_product_sale_packaging_price.row",
                {
                    packaging: packaging,
                    material_ids: this.materials,
                    currency: this.currency,
                }
            )
        );
    },
    add_packaging_empty: function (event) {
        this.add_packaging(this.empty_packaging());
        this.$placeholder.find(".row:last :input:first").focus()
    },
    delete_packaging: function (event) {
        return this.$(event.target).closest(".row").remove();
    },
});

return animation.registry.website_portal_purchase_product_sale_packaging_price;
});
