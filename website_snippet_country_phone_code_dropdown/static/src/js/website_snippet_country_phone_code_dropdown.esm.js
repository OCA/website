/* License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
import {CountryDropdown} from "@website_snippet_country_dropdown/js/website_snippet_country_dropdown.esm";
import {registry} from "@web/core/registry";

export class CountryPhoneCodeDropdown extends CountryDropdown {
    static selector = ".js_country_phone_code_dropdown";
    dynamicContent = {
        _root: {
            "t-on-shown.bs.dropdown": this.lazyImageLoad,
        },
        ".js_select_country_phone_code": {
            "t-on-click.prevent.withTarget": this.onClickCountry,
        },
        "#dropdown-countries": {
            "t-on-scroll": this.debounced(this.lazyImageLoad, 35),
        },
        ".js_no_country_field": {
            "t-on-change": this.onChangeNoCountryField,
        },
    };

    setup() {
        super.setup();
        this.btnCountryCodeEl = this.el.querySelector(".js_btn_country_phone_code");
        this.countryCodeFieldEl = this.el.querySelector(".js_country_phone_code_field");
    }

    onClickCountry(ev, currentTargetEl) {
        const phoneCode = currentTargetEl.dataset.country_phone_code;
        this.imgCodeEl.setAttribute("src", currentTargetEl.dataset.country_image_url);
        this.btnCountryCodeEl.dataset.country_phone_code = phoneCode;
        this.countryCodeFieldEl.value = "+" + phoneCode;
        this.joinValue(this.countryCodeFieldEl.value, this.noCountryFieldEl.value);
    }

    joinValue(phoneCode, value) {
        this.completeFieldPostEl.value = phoneCode.concat(" " + value);
    }
}

registry
    .category("public.interactions")
    .add(
        "website_snippet_country_phone_code_dropdown.country_phone_code_dropdown",
        CountryPhoneCodeDropdown
    );
