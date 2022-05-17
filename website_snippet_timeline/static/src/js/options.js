odoo.define("website_snippet_timeline.s_timeline_options", function(require) {
    "use strict";

    const options = require("web_editor.snippets.options");

    options.registry.Timeline = options.Class.extend({
        // --------------------------------------------------------------------------
        // Options
        // --------------------------------------------------------------------------
        /**
         * @override
         */
        _onLinkClick: function(ev) {
            if (!ev.isDefaultPrevented()) {
                const $timelineRow = this.$target.closest(".s_timeline_row");
                $timelineRow.toggleClass("flex-row-reverse flex-row");
            }
            return this._super.apply(this, arguments);
        },
    });
});
