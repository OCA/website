import {_t} from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import {renderToElement} from "@web/core/utils/render";
import {rpc} from "@web/core/network/rpc";
import {session} from "@web/session";

publicWidget.registry.follow.include({
    /**
     * @override
     */
    start() {
        const res = this._super(...arguments);
        if (!session.turnstile_site_key || this.editableMode) {
            return res;
        }
        if (!this.el.querySelector(".s_turnstile_container")) {
            const turnstileNodes = this._addTurnstile("website_mail_follow");
            turnstileNodes?.appendTo($(this.el));
            this._renderTurnstile(turnstileNodes);
        }
        return res;
    },

    _addTurnstile(action) {
        const mode =
            new URLSearchParams(window.location.search).get("cf") === "show"
                ? "always"
                : "interaction-only";
        const turnstileContainer = renderToElement(
            "website_cf_turnstile.turnstile_container",
            {
                action: action,
                appearance: mode,
                additionalClasses: "position-absolute top-0 start-0",
                beforeInteractiveGlobalCallback: "turnstileFollowBecomeVisible",
                errorGlobalCallback: "throwTurnstileErrorCode",
                executeGlobalCallback: "turnstileFollowSuccess",
                expiredCallback: "turnstileFollowExpired",
                sitekey: session.turnstile_site_key,
                style: "display: none; width: 0; height: 0; overflow: hidden;",
            }
        );
        let toInsert = $(turnstileContainer);
        globalThis.throwTurnstileErrorCode = function (code) {
            const error = new Error("Turnstile Error");
            error.code = code;
            throw error;
        };
        if (!window.turnstile?.render) {
            const turnstileScript = renderToElement(
                "website_cf_turnstile.turnstile_remote_script"
            );
            toInsert = toInsert.add($(turnstileScript));
        }
        return toInsert;
    },

    _renderTurnstile(turnstileNodes) {
        const nodes = turnstileNodes.toArray();
        const turnstileContainer = nodes.find((node) =>
            node.classList.contains("s_turnstile_container")
        );
        const turnstileScript = nodes.find(
            (node) => node.id === "s_turnstile_remote_script"
        );
        if (turnstileScript) {
            return;
        }
        if (
            window.turnstile?.render &&
            turnstileContainer &&
            !turnstileContainer.querySelector("iframe")
        ) {
            window.turnstile.render(turnstileContainer);
        }
    },

    /**
     * @override
     */
    async _onClick(ev) {
        const $jsFollow = $(ev.currentTarget).closest(".js_follow");
        const $email = $jsFollow.find(".js_follow_email");
        if ($email.length && !$email.val().match(/.+@.+/)) {
            $jsFollow
                .addClass("o_has_error")
                .find(".form-control, .form-select")
                .addClass("is-invalid");
            return false;
        }
        $jsFollow
            .removeClass("o_has_error")
            .find(".form-control, .form-select")
            .removeClass("is-invalid");
        const email = $email.length ? $email.val() : false;
        if (email || this.isUser) {
            const tokenCaptcha = await this._recaptcha.getToken("website_mail_follow");
            const token = tokenCaptcha.token;
            if (tokenCaptcha.error) {
                this.notification.add(tokenCaptcha.error, {
                    type: "danger",
                    title: _t("Error"),
                    sticky: true,
                });
                return false;
            }
            rpc("/website_mail/follow", {
                id: Number($jsFollow.data("id")),
                object: $jsFollow.data("object"),
                message_is_follower: $jsFollow.attr("data-follow") || "off",
                email: email,
                recaptcha_token_response: token,
                turnstile_captcha: this.$el
                    .find("input[name='turnstile_captcha']")
                    .val(),
            }).then((follow) => {
                this._toggleSubscription(follow, email, $jsFollow);
                const turnstileContainer = this.el.querySelector(
                    ".s_turnstile_container"
                );
                if (window.turnstile?.reset && turnstileContainer) {
                    window.turnstile.reset(turnstileContainer);
                }
            });
        }
    },
});
