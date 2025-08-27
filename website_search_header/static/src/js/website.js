/* global document, window */
(function () {
    "use strict";
    function mobileSearch() {
        if (!this.$boxInput.hasClass("d-none")) {
            this.$boxInput.addClass("d-none");
        }
        var searchQuery = document.querySelector("input[name='search']").value;
        var encodedQuery = encodeURIComponent(searchQuery);
        var searchURL = this._getSearchUrl(encodedQuery);
        window.location.href = searchURL;
    }

    function desktopSearch() {
        if ($(".o_search_header").hasClass("d-lg-none")) {
            $(".o_search_header").removeClass("d-lg-none");
            $("#search_btn_toggle_search i").removeClass("oi-search");
            $("#search_btn_toggle_search i").addClass("oi-close");
            $("#div_search_header").removeClass("ms-lg-0");
            $("#div_search_button").removeClass("ms-lg-2");
            $("input.oe_search_box").focus();
        } else {
            $(".o_search_header").addClass("d-lg-none");
            $("#search_btn_toggle_search i").removeClass("oi-close");
            $("#search_btn_toggle_search i").addClass("oi-search");
            $("#div_search_header").addClass("ms-lg-0");
            $("#div_search_button").addClass("ms-lg-2");
        }
    }

    function searchHeader() {
        var screenWidth =
            window.innerWidth ||
            document.documentElement.clientWidth ||
            document.body.clientWidth;
        if (screenWidth < 992) {
            mobileSearch();
        } else {
            desktopSearch();
        }
    }

    window.searchHeader = searchHeader;
})();
