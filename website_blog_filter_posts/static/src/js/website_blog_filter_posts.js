odoo.define('website_blog_filter_posts.website_blog_filter_posts', function(require) {

    "use strict";

    var animation = require('web_editor.snippets.animation');
    var utils = require('web.utils');

    animation.registry.blog_filter_selector = animation.Class.extend({
        selector: "#blog_filter_selector",

        start: function() {
            var stored_filter = utils.get_cookie('bp_filter_by_date');
            if (stored_filter) {
                $("#blog_filter_selector").val(stored_filter);
            }

            $("#blog_filter_selector").change(function() {
                var selected_filter = $('#blog_filter_selector').val();
                var ttl = 24*60*60*365;
                utils.set_cookie('bp_filter_by_date', selected_filter, ttl);

                window.location.reload();
            });
        },
    });

    animation.registry.blog_posts_selector = animation.Class.extend({
        selector: "#blog_posts_selector",

        start: function() {
            var stored_bpp = utils.get_cookie('bp_filter_by_bpp');

            if (stored_bpp) {
                $("#blog_posts_selector").val(stored_bpp);
            }

            $("#blog_posts_selector").change(function() {
                var selected_bpp = $("#blog_posts_selector").val();
                var ttl = 24*60*60*365;
                utils.set_cookie('bp_filter_by_bpp', selected_bpp);

                window.location.reload();
            });
        },

    });

    animation.registry.blog_posts_year_selector = animation.Class.extend({
        selector: "#blog_posts_year_selector",

        start: function() {
            var stored_year = utils.get_cookie('bp_filter_by_year');
            if (stored_year) {
                $("#blog_posts_year_selector").val(stored_year);
            }

            $("#blog_posts_year_selector").change(function() {
                var selected_year = $("#blog_posts_year_selector").val();

                if (isNaN(selected_year)) {
                    alert('Please select a Year.');
                    return;
                }

                var ttl = 24*60*60*365;
                utils.set_cookie('bp_filter_by_year', selected_year);

                window.location.reload();
            });
        },
    });

});