odoo.define("website_mass_mailing.tour.test_newsletter_popup", function (require) {
    "use strict";

    const tour = require("web_tour.tour");
    const wTourUtils = require("website.tour_utils");

    tour.register(
        "test_newsletter_popup",
        {
            test: true,
            url: "/?enable_editor=1",
        },
        [
            wTourUtils.dragNDrop({
                id: "s_newsletter_subscribe_popup",
                name: "Newsletter Popup",
            }),
            {
                content: "Check the modal is opened for edition",
                trigger: ".o_newsletter_popup .modal:visible",
                in_modal: false,
                run: () => null,
            },
            ...wTourUtils.clickOnSave(),
            {
                content: "Check the modal has been saved, closed",
                trigger: ".o_newsletter_popup",
                extra_trigger: "body:not(.editor_enable)",
                run: function () {
                    const $modal = this.$anchor.find(".modal");
                    if ($modal.is(":visible")) {
                        console.error("Modal is still opened...");
                    }
                },
            },
        ]
    );
});
odoo.define("website_mass_mailing.tour.test_double_optin_popup", function (require) {
    "use strict";

    const tour = require("web_tour.tour");

    tour.register(
        "test_double_optin_popup",
        {
            test: true,
            url: "/",
        },
        [
            {
                content: "Check the modal is not yet opened and force it opened",
                trigger: ".o_newsletter_popup",
                run: function () {
                    const $modal = this.$anchor.find(".modal");
                    if ($modal.is(":visible")) {
                        console.error("Modal is already opened...");
                    }
                    $(document).trigger("mouseleave");
                },
            },
            {
                content:
                    "Check the modal is now opened and enter text in the subscribe input",
                trigger: ".o_newsletter_popup .modal input",
                in_modal: false,
                run: "text hello@world.com",
            },
            {
                content: "Subscribe",
                trigger: ".modal-dialog .js_subscribe_btn",
            },
            {
                content: "Check the modal is now closed",
                trigger: ".o_newsletter_popup",
                run: function () {
                    const $modal = this.$anchor.find(".modal");
                    if ($modal.is(":visible")) {
                        console.error("Modal is still opened...");
                    }
                },
            },
        ]
    );
});
