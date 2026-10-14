// Hosts handled by Odoo itself through an <iframe> player.
const PLATFORM_HOSTS = [
    "youtu.be",
    "youtube.com",
    "youtube-nocookie.com",
    "vimeo.com",
    "dailymotion.com",
    "dai.ly",
    "instagram.com",
    "instagr.am",
    "facebook.com",
];

// Player options stored in the video URL (see tools.py on the server side).
const OPTION_PARAMS = {
    "autoplay=1": "autoplay",
    "loop=1": "loop",
    "controls=0": "hideControls",
};

/**
 * Returns the HTML5 player data for a video URL saved by the editor, or null
 * when the URL belongs to a platform rendered with an <iframe>.
 *
 * Only URLs that went through the server-side check end up in the page with a
 * non-platform host, so no extension or host allow-list check is needed here.
 *
 * @param {String} src
 * @returns {{src: string, autoplay: boolean, loop: boolean, hideControls: boolean}|null}
 */
export function getHtml5VideoData(src) {
    const match = (src || "").trim().match(/^(?:https?:)?\/\/([^/?#:]+)/i);
    if (!match) {
        return null;
    }
    const host = match[1].toLowerCase().replace(/^www\./, "");
    if (PLATFORM_HOSTS.some((h) => host === h || host.endsWith(`.${h}`))) {
        return null;
    }
    const data = {autoplay: false, loop: false, hideControls: false};
    // Strip our option pairs with string operations: re-encoding the query
    // string could break signed CDN URLs.
    const [base, ...fragment] = src.trim().split("#");
    const [path, query] = base.split(/\?(.*)/s);
    const kept = [];
    for (const pair of (query || "").split("&").filter(Boolean)) {
        if (pair in OPTION_PARAMS) {
            data[OPTION_PARAMS[pair]] = true;
        } else {
            kept.push(pair);
        }
    }
    data.src =
        path +
        (kept.length ? `?${kept.join("&")}` : "") +
        (fragment.length ? `#${fragment.join("#")}` : "");
    return data;
}

/**
 * Builds a <video> element for HTML5 player data.
 *
 * @param {Object} data result of `getHtml5VideoData`
 * @param {Object} [options]
 * @param {Boolean} [options.background] muted looping video without controls
 * @returns {HTMLVideoElement}
 */
export function buildHtml5VideoEl(data, {background = false} = {}) {
    const videoEl = document.createElement("video");
    videoEl.classList.add("o_video_html5");
    videoEl.setAttribute("playsinline", "");
    const autoplay = background || data.autoplay;
    if (autoplay) {
        // Browsers only allow autoplay for muted videos.
        videoEl.setAttribute("autoplay", "");
        videoEl.setAttribute("muted", "");
        videoEl.muted = true;
    }
    if (background || data.loop) {
        videoEl.setAttribute("loop", "");
    }
    if (!background && !data.hideControls) {
        videoEl.setAttribute("controls", "");
    }
    videoEl.setAttribute("preload", autoplay ? "auto" : "metadata");
    videoEl.setAttribute("src", data.src);
    return videoEl;
}
