import {buildHtml5VideoEl, getHtml5VideoData} from "./html5_video_utils.esm";
import {MediaVideo} from "@website/interactions/video/media_video";
import {patch} from "@web/core/utils/patch";

patch(MediaVideo.prototype, {
    setup() {
        super.setup();
        this.html5Video = getHtml5VideoData(
            this.el.dataset.oeExpression || this.el.dataset.src
        );
        if (this.html5Video) {
            // Self-hosted videos do not load third-party cookies.
            this.cookiesAccepted = true;
            this.dynamicContent = {
                ...this.dynamicContent,
                _popup: {
                    "t-on-hide.bs.modal": () =>
                        this.el.querySelector(":scope > video")?.pause(),
                },
            };
        }
    },

    start() {
        if (!this.html5Video) {
            return super.start();
        }
        if (this.el.querySelector(":scope > video")) {
            return;
        }
        // The video is part of the saved content (no cleanup on purpose), as
        // the <iframe> is for other platforms.
        const extraEditionEl = document.createElement("div");
        extraEditionEl.className = "css_editable_mode_display";
        const extraSizeEl = document.createElement("div");
        extraSizeEl.className = "media_iframe_video_size";
        this.el.replaceChildren(
            extraEditionEl,
            extraSizeEl,
            buildHtml5VideoEl(this.html5Video)
        );
    },
});
