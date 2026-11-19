import {
    clickOnSave,
    insertSnippet,
    registerWebsitePreviewTour,
} from "@website/js/tours/tour_utils";
import {registry} from "@web/core/registry";

const VIDEO_PATH = "/website_media_video_html5/static/tests/sample.webm";

registerWebsitePreviewTour(
    "website_media_video_html5_editor",
    {
        url: "/",
        edition: true,
    },
    () => [
        ...insertSnippet({
            id: "s_text_image",
            name: "Text - Image",
            groupName: "Content",
        }),
        {
            content: "Select the image",
            trigger:
                ":iframe #wrap .s_text_image img, :iframe #wrap .s_text_image img:not(:visible)",
            run: "click",
        },
        {
            content: "Click on replace media",
            trigger: "[data-action-id='replaceMedia']",
            run: "click",
        },
        {
            content: "Open the videos tab",
            trigger: "a:contains('Videos')",
            run: "click",
        },
        {
            content: "Enter the URL of a video file",
            trigger: "#o_video_text",
            run() {
                this.anchor.value = `${window.location.origin}${VIDEO_PATH}`;
                this.anchor.dispatchEvent(new Event("input", {bubbles: true}));
            },
        },
        {
            content: "The URL is accepted and previewed with an HTML5 player",
            trigger: "#o_video_text.is-valid",
        },
        {
            content: "Check the preview",
            trigger: `video.o_video_dialog_iframe[src*='${VIDEO_PATH}']`,
        },
        {
            content: "Enable the loop option",
            trigger: ".o_video_dialog_options .o_switch:contains('Loop') input",
            run: "click",
        },
        {
            content: "Wait for the option to be stored in the URL",
            trigger: "#o_video_text:value(/loop=1/)",
        },
        {
            content: "Add the video",
            trigger: ".modal-footer button:contains('Add'):not([disabled])",
            run: "click",
        },
        {
            content: "The video block contains an HTML5 player",
            trigger: `:iframe #wrap .media_iframe_video > video.o_video_html5[loop][src*='${VIDEO_PATH}']`,
        },
        ...clickOnSave(),
        {
            content: "The saved page renders the HTML5 player",
            trigger: `:iframe #wrap .media_iframe_video > video.o_video_html5[loop][controls][src$='${VIDEO_PATH}']`,
        },
    ]
);

registerWebsitePreviewTour(
    "website_media_video_html5_background",
    {
        url: "/",
        edition: true,
    },
    () => [
        ...insertSnippet({
            id: "s_text_image",
            name: "Text - Image",
            groupName: "Content",
        }),
        {
            content: "Select the section",
            trigger: ":iframe #wrap .s_text_image",
            run: "click",
        },
        {
            content: "Skip the Vimeo suggestions, external requests fail in tests",
            trigger: "body",
            run() {
                const {VideoSelector} = odoo.loader.modules.get(
                    "@html_editor/main/media/media_dialog/video_selector"
                );
                VideoSelector.prototype.prepareVimeoPreviews = () => Promise.resolve();
            },
        },
        {
            content: "Enable the background video",
            trigger: "[data-action-id='toggleBgVideo']",
            run: "click",
        },
        {
            content: "Enter the URL of a video file",
            trigger: ".modal #o_video_text",
            run() {
                this.anchor.value = `${window.location.origin}${VIDEO_PATH}`;
                this.anchor.dispatchEvent(new Event("input", {bubbles: true}));
            },
        },
        {
            content: "Check the preview",
            trigger: `.modal video.o_video_dialog_iframe[src*='${VIDEO_PATH}']`,
        },
        {
            content: "Use the video as background",
            trigger: ".modal-footer button:contains('Add'):not([disabled])",
            run: "click",
        },
        {
            content: "The section has an HTML5 background video",
            trigger: `:iframe #wrap .s_text_image.o_background_video[data-bg-video-src*='${VIDEO_PATH}'] > .o_bg_video_container > video.o_bg_video_html5[autoplay][muted][loop]`,
        },
        ...clickOnSave(),
        {
            content: "The saved page renders the HTML5 background video",
            trigger: `:iframe #wrap .s_text_image.o_background_video > .o_bg_video_container > video.o_bg_video_html5[src$='${VIDEO_PATH}']`,
        },
    ]
);

registry.category("web_tour.tours").add("website_media_video_html5_public", {
    steps: () => [
        {
            content: "Inline video file is rendered with an HTML5 player",
            trigger: `#wrap .o_test_inline .media_iframe_video > video.o_video_html5[autoplay][muted][src$='${VIDEO_PATH}']`,
        },
        {
            content: "Inline video keeps its controls",
            trigger: "#wrap .o_test_inline video.o_video_html5[controls]",
        },
        {
            content: "Background video is rendered with an HTML5 player",
            trigger: `#wrap .o_test_background > .o_bg_video_container > video.o_bg_video_html5[autoplay][muted][loop][playsinline][src$='${VIDEO_PATH}']`,
        },
        {
            content: "Background video has no controls",
            trigger: "#wrap .o_test_background video.o_bg_video_html5:not([controls])",
        },
        {
            content: "Other platforms still use an iframe",
            trigger:
                "#wrap .o_test_youtube .media_iframe_video > iframe[src*='youtube']",
        },
    ],
});
