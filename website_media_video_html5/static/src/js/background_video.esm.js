import {buildHtml5VideoEl, getHtml5VideoData} from "./html5_video_utils.esm";
import {BackgroundVideo} from "@website/interactions/video/background_video";
import {patch} from "@web/core/utils/patch";

patch(BackgroundVideo.prototype, {
    setup() {
        super.setup();
        this.html5Video = getHtml5VideoData(this.videoSrc);
        if (this.html5Video) {
            // No third-party cookies involved: nothing to wait for.
            this.dynamicContent = {...this.dynamicContent, _document: {}};
        }
    },

    adjustIframe() {
        // The <video> covers its container with CSS (object-fit).
        if (!this.html5Video) {
            return super.adjustIframe();
        }
    },

    appendBgVideo() {
        if (!this.html5Video) {
            return super.appendBgVideo();
        }
        const oldContainer =
            this.bgVideoContainer ||
            this.el.querySelector(":scope > .o_bg_video_container");
        oldContainer?.remove();

        const containerEl = document.createElement("div");
        containerEl.className = "o_bg_video_container";
        const videoEl = buildHtml5VideoEl(this.html5Video, {background: true});
        videoEl.id = this.iframeID;
        videoEl.classList.add("o_bg_video_iframe", "o_bg_video_html5");
        videoEl.setAttribute("aria-hidden", "true");
        containerEl.appendChild(videoEl);
        this.insert(containerEl, this.el, "afterbegin");

        this.bgVideoContainer = containerEl;
        this.iframeEl = videoEl;
    },
});
