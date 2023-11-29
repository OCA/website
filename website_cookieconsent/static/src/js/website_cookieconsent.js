$(function() {
    "use strict";

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

    function isValidJSON(str) {
        try {
            JSON.parse(str);
            return true;
        } catch (e) {
            return false;
        }
    }

    $.ajax({
        type: 'POST',
        url: '/website_cookieconsent',
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('Content-Type', 'application/json');
        },
        data: JSON.stringify({
            jsonrpc: '2.0'
        }),
        success: function(data) {
            if (data && 'result' in data && 'cookie_config' in
                data['result']) {
                let options = data['result']['cookie_config'];
                if (options !== '' && isValidJSON(options)) {
                    let opts = JSON.parse(options);
                    if ('language' in opts) {
                        opts['language']['default'] = extractLanguageFromCookie(
                        document.cookie);
                    }
                    CookieConsent.run(opts);
                }
            }
        }
    });
})