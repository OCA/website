(function () {
    "use strict";

    openerp.website.dom_ready.then(function () {
        function extractLanguageFromCookie(cookieString) {
            const cookies = cookieString.split(';');
            let lang = null;

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                const [cookieName, cookieValue] = cookie.split('=');

                if (cookieName === 'website_lang') {
                    let langValue = cookieValue.split('_')[0];
                    lang = langValue.toLowerCase();
                    break;
                }
            }

            return lang;
        }

        class Analytics {
            init() {
                this.events = document.querySelectorAll('[data-ga4-event]');
                this.events.forEach(((ev) => {
                    ev.addEventListener('click', ({ currentTarget }) => {
                        const target = currentTarget;
                        if (target) {
                            const analyticsData = {};
                            Object.entries(target.dataset).forEach((e) => {
                                const key = e[0];
                                const value = e[1];
                                const m = key.match('ga4Param(.+)');
                                if (m && m[1]) {
                                    analyticsData[this.unCamelCase(m[1], '_')] = value;
                                }
                            });
                            this.sendEvent(target.dataset.ga4Event, analyticsData);
                        }
                    });
                }));
            }

            unCamelCase(str, separator = '_') {
                return str.replace(/([a-z\d])([A-Z])/g, `$1${separator}$2`).replace(/([A-Z]+)([A-Z][a-z\d]+)/g, `$1${separator}$2`).toLowerCase();
            }

            sendEvent(name, data) {
                if (typeof gtag !== 'undefined') {
                    gtag('event', name, data);
                }
            }
        }

        openerp.jsonRpc('/website_cookieconsent', 'call', {}).then((data) => {
            let x_iframemanager = iframemanager();
            let x_analytics = new Analytics();
            if (data && 'cookie_config' in data && 'iframemanager_config' in data) {
                let cookie_options = data['cookie_config'];
                let iframemanager_options = data['iframemanager_config'];
                let lang = extractLanguageFromCookie(document.cookie);

                if (iframemanager_options !== '') {
                    let iframe_opts = eval(iframemanager_options);
                    if ('currLang' in iframe_opts) {
                        iframe_opts['currLang'] = lang;
                    }
                    x_iframemanager.run(iframe_opts);
                }

                if (cookie_options !== '') {
                    let cookie_opts = eval(cookie_options);
                    if ('language' in cookie_opts) {
                        cookie_opts['language']['default'] = lang;
                    }
                    CookieConsent.run(cookie_opts);
                }
            }
        });
    })
}())