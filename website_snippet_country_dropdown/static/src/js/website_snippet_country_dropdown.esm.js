/* Copyright 2016 Tecnativa, S.L.
 * Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * Copyright 2019 Alexandre Díaz <alexandre.diaz@tecnativa.com>
 * Copyright 2025 Tecnativa - Pilar Vargas
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";

export class CountryDropdown extends Interaction {
    static selector = ".js_country_dropdown";
    dynamicContent = {
        _root: {
            "t-on-shown.bs.dropdown": this.lazyImageLoad,
        },
        ".js_select_country_code": {
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
        this.imgCodeEl = this.el.querySelector(".js_img_country_code");
        this.btnCountryCodeEl = this.el.querySelector(".js_btn_country_code");
        this.dropdownListEl = this.el.querySelector("#dropdown-countries");
        this.countryCodeFieldEl = this.el.querySelector(".js_country_code_field");
        this.noCountryFieldEl = this.el.querySelector(".js_no_country_field");
        this.completeFieldPostEl = this.el.querySelector(".js_complete_field_post");
    }

    onClickCountry(ev, currentTargetEl) {
        const countryCode = currentTargetEl.dataset.country_code;
        this.imgCodeEl.setAttribute("src", currentTargetEl.dataset.country_image_url);
        this.btnCountryCodeEl.dataset.country_code = countryCode;
        this.countryCodeFieldEl.value = countryCode;
        this.joinValue(countryCode, this.noCountryFieldEl.value);
    }

    onChangeNoCountryField() {
        this.joinValue(this.countryCodeFieldEl.value, this.noCountryFieldEl.value);
    }

    joinValue(countryCode, value) {
        this.completeFieldPostEl.value = countryCode.concat(value);
    }

    isOptionVisible(el) {
        const listRect = this.dropdownListEl.getBoundingClientRect();
        const elRect = el.getBoundingClientRect();
        return elRect.top <= listRect.bottom && elRect.bottom >= listRect.top;
    }

    lazyImageLoad() {
        for (const optionEl of this.dropdownListEl.querySelectorAll(":scope > a")) {
            const imgEl = optionEl.querySelector("img");
            if (!imgEl.getAttribute("src") && this.isOptionVisible(optionEl)) {
                imgEl.setAttribute("src", optionEl.dataset.country_image_url);
            }
        }
    }
}

registry
    .category("public.interactions")
    .add("website_snippet_country_dropdown.country_dropdown", CountryDropdown);
