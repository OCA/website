odoo.define("website_search_header.search_header", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");

    publicWidget.registry.SearchHeader = publicWidget.Widget.extend({
        selector: "#div_search_button",

        events: {
            "click  #search_btn_toggle_search": "_onClickSearchBtn",
        },

        start: function () {
            const def = this._super.apply(this, arguments);
            this.$boxInput = this.$el.find(".o_search_header");
            return def;
        },

        mobileSearch: function () {
            if (!this.$boxInput.hasClass("d-none")) {
                this.$boxInput.addClass("d-none");
            }
            var searchQuery = document.querySelector("input[name='search']").value;
            var encodedQuery = encodeURIComponent(searchQuery);
            var searchURL = this._getSearchUrl(encodedQuery);
            window.location.href = searchURL;
        },

        desktopSearch: function () {
            if (!$(".o_search_header").hasClass("d-lg-none")) {
                $(".o_search_header").addClass("d-lg-none");
                $("#search_btn_toggle_search i").removeClass("oi-close");
                $("#search_btn_toggle_search i").addClass("oi-search");
                $("#div_search_header").addClass("ms-lg-0");
                $("#div_search_button").addClass("ms-lg-2");
            } else {
                $(".o_search_header").removeClass("d-lg-none");
                $("#search_btn_toggle_search i").removeClass("oi-search");
                $("#search_btn_toggle_search i").addClass("oi-close");
                $("#div_search_header").removeClass("ms-lg-0");
                $("#div_search_button").removeClass("ms-lg-2");
                $("input.oe_search_box").focus();
            }
        },

        _onClickSearchBtn: function () {
            var screenWidth =
                window.innerWidth ||
                document.documentElement.clientWidth ||
                document.body.clientWidth;
            if (screenWidth < 992) {
                this.mobileSearch();
            } else {
                this.desktopSearch();
            }
        },

        _getSearchUrl: function (encodedQuery) {
            return "/website/search?search=" + encodedQuery + "&amp;order=name+asc";
        },
    });
});
