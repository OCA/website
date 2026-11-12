import {BaseOptionComponent} from "@html_builder/core/utils";
import {Plugin} from "@html_editor/plugin";
import {registry} from "@web/core/registry";

export class MobileBarItemOption extends BaseOptionComponent {
    static template = "website_snippet_bottom_mobile_button.MobileBarItemOption";
    static selector = ".s_mobile_bar_item";
}

export class MobileBarOption extends BaseOptionComponent {
    static template = "website_snippet_bottom_mobile_button.MobileBarOption";
    static selector = ".o_mobile_bottom_bar";
    static editableOnly = false;
}

class MobileBarOptionPlugin extends Plugin {
    static id = "mobileBarOption";
    resources = {
        builder_options: [MobileBarItemOption, MobileBarOption],
        dropzone_selector: {
            selector: ".s_mobile_bar_item",
            dropNear: ".s_mobile_bar_item",
            dropIn: ".o_mobile_bar_row:not(:has(> .s_mobile_bar_item))",
        },
        legit_empty_link_predicates: (linkEl) =>
            linkEl.classList.contains("o_mobile_bar_link"),
    };
}

registry
    .category("website-plugins")
    .add(MobileBarOptionPlugin.id, MobileBarOptionPlugin);
