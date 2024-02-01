(function() {
    "use strict";

    openerp.website.dom_ready.then(function() {
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

        openerp.jsonRpc('/website_cookieconsent', 'call', {}).then((data) => {
            let iframe_manager = iframemanager();
            if (data && 'cookie_config' in data && 'iframemanager_config' in data) {
                let cookie_options = data['cookie_config'];
                let iframemanager_options = data['iframemanager_config'];
                let lang = extractLanguageFromCookie(document.cookie);

                if (iframemanager_options !== '') {
                    let iframe_opts = eval(iframemanager_options);
                    if ('currLang' in iframe_opts) {
                        iframe_opts['currLang'] = lang;
                    }
                    iframe_manager.run(iframe_opts);
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