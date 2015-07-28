/* © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

"use strict";
(function ($) {
    openerp.Tour.register({
        id: "marginless_gallery",
        name: "Insert a marginless gallery snippet",
        path: "/page/homepage",
        mode: "test",
        steps: [
            {
                title: "Edit the homepage (1)",
                waitFor: "button[data-action=edit]",
                element: "button[data-action=edit]",
            },
            {
                title: "Click on Insert Blocks (1)",
                waitFor: "button[data-action=snippet]",
                element: "button[data-action=snippet]",
            },
            {
                title: "Click on Features (1)",
                waitFor: "a[href='#snippet_feature']",
                element: "a[href='#snippet_feature']",
            },
            {
                title: "Drag and drop a marginless gallery snippet (1)",
                waitFor: ".oe_snippet:contains('Marginless Gallery'):visible",
                snippet: ".oe_snippet:contains('Marginless Gallery')",
            },
            {
                title: "Cancel modal dialog",
                waitFor: ".modal button:contains('Cancel'):visible",
                element: ".modal button:contains('Cancel'):visible",
            },
            {
                title: "Click on Insert Blocks (2)",
                waitNot: ".modal:visible, \
                          #oe_manipulators .btn:visible, \
                          #wrap .marginless-gallery:visible",
                waitFor: "button[data-action=snippet]",
                element: "button[data-action=snippet]",
            },
            {
                title: "Click on Features (2)",
                waitFor: "a[href='#snippet_feature']",
                element: "a[href='#snippet_feature']",
            },
            {
                title: "Drag and drop a marginless gallery snippet (2)",
                waitFor: ".oe_snippet:contains('Marginless Gallery'):visible",
                snippet: ".oe_snippet:contains('Marginless Gallery')",
            },
            {
                title: "Set no fixed height",
                waitFor: ".modal .btn-primary:visible",
                element: ".modal .btn-primary:visible",
            },
            {
                title: "Click on Customize",
                waitFor: "#wrap .marginless-gallery, \
                          .btn-primary:contains('Customize'):visible",
                element: ".btn-primary:contains('Customize'):visible",
            },
            {
                title: "Click on Change Images Height",
                waitFor: ".js_change_height:visible",
                element: ".js_change_height:visible",
            },
            {
                title: "Set image height of 200px",
                waitFor: ".modal input:visible",
                element: ".modal input:visible",
                sampleText: "200",
            },
            {
                title: "Accept modal dialog",
                waitFor: ".modal input:contains('200'):visible",
                element: ".modal .btn-primary:visible",
            },
            {
                title: "Check that the right height has been saved",
                waitNot: ".modal:visible",
                waitFor: "#wrap .marginless-gallery \
                          .col-md-3[style*='height: 200px']",
            },
        ],
    });
})(jQuery);
