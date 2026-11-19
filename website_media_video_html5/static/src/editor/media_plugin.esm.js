import {MediaPlugin} from "@html_editor/main/media/media_plugin";
import {patch} from "@web/core/utils/patch";

/**
 * The background video option reads the URL from the <iframe> of the selected
 * media: give it one for HTML5 videos. The element is never attached to the
 * document, so the URL is not loaded.
 *
 * @param {HTMLElement} media
 * @returns {HTMLElement}
 */
function withIframeCarrier(media) {
    const videoEl = media?.querySelector?.(":scope > video.o_video_html5");
    if (!videoEl || media.querySelector("iframe")) {
        return media;
    }
    const carrierEl = document.createElement("div");
    const iframeEl = document.createElement("iframe");
    iframeEl.src = videoEl.src;
    carrierEl.appendChild(iframeEl);
    return carrierEl;
}

patch(MediaPlugin.prototype, {
    openMediaDialog(params = {}, editableEl = null) {
        const save = params.save;
        if (!save || !params.visibleTabs?.includes("VIDEO_BACKGROUND")) {
            return super.openMediaDialog(params, editableEl);
        }
        return super.openMediaDialog(
            {
                ...params,
                save: (media, ...args) => save(withIframeCarrier(media), ...args),
            },
            editableEl
        );
    },
});
