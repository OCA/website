import {buildHtml5VideoEl, getHtml5VideoData} from "../js/html5_video_utils.esm";
import {VideoSelector} from "@html_editor/main/media/media_dialog/video_selector";
import {patch} from "@web/core/utils/patch";

const HTML5 = "html5";

patch(VideoSelector.prototype, {
    setup() {
        super.setup();
        this.PLATFORMS.html5 = HTML5;
        // Media fragments (#t=) set the start time, as for Vimeo.
        this.platformParams.html5 = "#t=";
        for (const optionId of ["autoplay", "loop", "hide_controls", "start_from"]) {
            this.OPTIONS[optionId].platforms.push(HTML5);
        }
    },

    get html5PreviewSrc() {
        return getHtml5VideoData(this.state.src)?.src || "";
    },
});

patch(VideoSelector, {
    createElements(selectedMedia) {
        const elements = super.createElements(...arguments);
        return elements.map((element, index) => {
            const video = selectedMedia[index];
            const data = video.platform === HTML5 && getHtml5VideoData(video.src);
            if (data) {
                element.classList.add("o_video_html5_wrapper");
                element
                    .querySelector(":scope > iframe")
                    .replaceWith(buildHtml5VideoEl(data));
            }
            return element;
        });
    },
});
