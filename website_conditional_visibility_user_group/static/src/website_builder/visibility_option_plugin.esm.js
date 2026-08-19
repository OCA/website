/*
   Copyrigt 2026 Tecnativa - Carlos Roca
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {registry} from "@web/core/registry";
import {Plugin} from "@html_editor/plugin";
import {selectElements} from "@html_editor/utils/dom_traversal";
import {withSequence} from "@html_editor/utils/resource";
import {VisibilityOption} from "@website/builder/plugins/options/visibility_option";

const LOGGED_IN_VALUE = "true";

class VisibilityGroupOptionPlugin extends Plugin {
    static id = "visibilityGroupOption";
    resources = {
        visibility_selector_parameters: [
            {
                saveAttribute: "visibilityUserGroup",
                attributeName: "data-user_group",
                callWith: "value",
            },
        ],
        normalize_handlers: withSequence(1, this.cleanUserGroup.bind(this)),
    };

    /**
     * The group restriction only makes sense on top of "Visible for Logged In".
     * Drop it as soon as that condition no longer holds, otherwise it would
     * keep hiding the snippet with no visible option to undo it.
     *
     * @param {HTMLElement} rootEl
     */
    cleanUserGroup(rootEl) {
        for (const el of selectElements(rootEl, VisibilityOption.selector)) {
            if (!el.dataset.visibilityUserGroup) {
                continue;
            }
            if (el.dataset.visibility !== "conditional" || !this.isLoggedInOnly(el)) {
                delete el.dataset.visibilityUserGroup;
            }
        }
    }

    isLoggedInOnly(el) {
        const logged = el.dataset.visibilityValueLogged;
        if (!logged || el.dataset.visibilityValueLoggedRule === "hide") {
            return false;
        }
        try {
            return JSON.parse(logged).some(
                (record) => String(record.value) === LOGGED_IN_VALUE
            );
        } catch {
            return false;
        }
    }
}

registry
    .category("website-plugins")
    .add(VisibilityGroupOptionPlugin.id, VisibilityGroupOptionPlugin);
