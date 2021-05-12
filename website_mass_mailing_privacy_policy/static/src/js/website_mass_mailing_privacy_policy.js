odoo.define("website_mass_mailing_privacy_policy.subscribe", function (require) {
    "use strict";
    require("mass_mailing.website_integration");
    var animation = require("website.content.snippets.animation");

    animation.registry.subscribe.include({
        _onClick: function() {
            var self = this;
            var $privacy_policy = this.$target.find(".js_subscribe_privacy_policy");
            if ($privacy_policy[0].checked) {
                $privacy_policy.removeClass('is-invalid');
            }
            else {
                $privacy_policy.addClass('is-invalid');
                return false;
            }
            return this._super.apply(this, arguments);
        },
    });

    animation.registry.newsletter_popup.include({
        _onClickSubscribe: function() {
            var self = this;
            var $privacy_policy = this.$target.find(".js_subscribe_popup_privacy_policy");
            if ($privacy_policy[0].checked) {
                $privacy_policy.removeClass('is-invalid');
            }
            else {
                $privacy_policy.addClass('is-invalid');
                return false;
            }
            return this._super.apply(this, arguments);
        },
    });
});
