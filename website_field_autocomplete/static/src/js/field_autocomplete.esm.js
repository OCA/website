import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";

let nextMenuId = 0;

export class FieldAutocomplete extends Interaction {
    static selector = ".js_website_autocomplete";

    async start() {
        const result = await super.start();
        const data = this.el.dataset;
        this.model = data.model;
        this.queryField = data.queryField || "name";
        this.displayField = data.displayField || this.queryField;
        this.field = data.field || "";
        this.valueField = data.valueField || this.displayField;
        this.limit = Number.parseInt(data.limit, 10) || 10;
        this.additionalDomain = this._parseDomain(data.domain);
        this.fields = Array.from(new Set([this.displayField, this.valueField]));
        this.items = [];
        this.activeIndex = -1;
        this.requestId = 0;
        this.search = this.debounced(() => this._search(), 300);

        this._setupInput();
        this._setupMenu();

        this.addListener(this.el, "input", () => this._onInput());
        this.addListener(this.el, "keydown", (event) => this._onKeydown(event));
        this.addListener(this.menu, "click", (event) => this._onMenuClick(event));
        this.addListener(this.el.ownerDocument, "mousedown", (event) =>
            this._onDocumentMouseDown(event)
        );
        return result;
    }

    destroy() {
        if (this.wrapper && this.wrapper.parentNode) {
            this.wrapper.replaceWith(this.el);
        }
    }

    _setupInput() {
        this.el.setAttribute("autocomplete", "off");
        this.el.setAttribute("aria-autocomplete", "list");
        this.el.setAttribute("aria-expanded", "false");
        this.el.setAttribute("role", "combobox");

        const wrapper = this.el.ownerDocument.createElement("div");
        wrapper.className = "position-relative";
        this.el.replaceWith(wrapper);
        wrapper.append(this.el);
        this.wrapper = wrapper;
    }

    _setupMenu() {
        const menu = this.el.ownerDocument.createElement("div");
        menu.className = "dropdown-menu w-100";
        menu.hidden = true;
        menu.setAttribute("role", "listbox");
        menu.id = "field_autocomplete_menu_" + ++nextMenuId;
        this.wrapper.append(menu);
        this.menu = menu;
        this.el.setAttribute("aria-controls", menu.id);
    }

    _parseDomain(domain) {
        if (!domain) {
            return [];
        }
        try {
            const parsedDomain = JSON.parse(domain);
            return Array.isArray(parsedDomain) ? parsedDomain : [];
        } catch {
            return [];
        }
    }

    async _search() {
        const term = this.el.value.trim();
        const requestId = ++this.requestId;
        if (!term || !this.model) {
            this._hideMenu();
            return;
        }

        const domain = [[this.queryField, "ilike", term]].concat(this.additionalDomain);
        try {
            const records = await this.waitFor(
                rpc("/website/field_autocomplete/" + encodeURIComponent(this.model), {
                    domain,
                    fields: this.fields,
                    limit: this.limit,
                })
            );
            if (requestId !== this.requestId || term !== this.el.value.trim()) {
                return;
            }
            this._renderSuggestions(records);
        } catch {
            if (requestId === this.requestId) {
                this._hideMenu();
            }
        }
    }

    _renderSuggestions(records) {
        this.menu.replaceChildren();
        this.items = [];
        this.activeIndex = -1;

        for (const record of records || []) {
            const label = record[this.displayField];
            if (label === undefined || label === null) {
                continue;
            }

            const option = this.el.ownerDocument.createElement("button");
            option.type = "button";
            option.className = "dropdown-item text-truncate";
            option.setAttribute("role", "option");
            option.setAttribute("aria-selected", "false");
            option.dataset.index = String(this.items.length);
            option.id = this.menu.id + "_option_" + this.items.length;
            option.textContent = String(label);
            this.menu.append(option);
            this.items.push({
                element: option,
                label: String(label),
                value: record[this.valueField],
            });
        }

        if (this.items.length) {
            this._showMenu();
        } else {
            this._hideMenu();
        }
    }

    _onInput() {
        this.requestId++;
        this._clearMany2OneValue();
        this._hideMenu();
        if (this.el.value.trim()) {
            this.search();
        }
    }

    _onKeydown(event) {
        if (event.key === "ArrowDown" && this.items.length) {
            event.preventDefault();
            this._setActiveItem(this.activeIndex + 1);
        } else if (event.key === "ArrowUp" && this.items.length) {
            event.preventDefault();
            this._setActiveItem(this.activeIndex - 1);
        } else if (
            event.key === "Enter" &&
            this.activeIndex >= 0 &&
            this.items.length
        ) {
            event.preventDefault();
            this._selectItem(this.activeIndex);
        } else if (event.key === "Escape") {
            this._hideMenu();
        }
    }

    _onMenuClick(event) {
        const option = event.target.closest("[data-index]");
        if (!option || !this.menu.contains(option)) {
            return;
        }
        this._selectItem(Number.parseInt(option.dataset.index, 10));
    }

    _onDocumentMouseDown(event) {
        if (!this.wrapper.contains(event.target)) {
            this._hideMenu();
        }
    }

    _setActiveItem(requestedIndex) {
        this.items[this.activeIndex]?.element.setAttribute("aria-selected", "false");
        let index = requestedIndex;
        if (index >= this.items.length) {
            index = 0;
        } else if (index < 0) {
            index = this.items.length - 1;
        }
        this.activeIndex = index;
        const item = this.items[index];
        item.element.classList.add("active");
        item.element.setAttribute("aria-selected", "true");
        this.items.forEach((candidate, candidateIndex) => {
            if (candidateIndex !== index) {
                candidate.element.classList.remove("active");
            }
        });
        this.el.setAttribute("aria-activedescendant", item.element.id);
    }

    _selectItem(index) {
        const item = this.items[index];
        if (!item) {
            return;
        }
        this.el.value = item.label;
        this._setMany2OneValue(item.value);
        this._hideMenu();
        this.el.dispatchEvent(new Event("change", {bubbles: true}));
    }

    _setMany2OneValue(value) {
        if (!this.field || !this.el.form) {
            return;
        }
        let field = this.el.form.elements.namedItem(this.field);
        if (!field) {
            field = this.el.ownerDocument.createElement("input");
            field.type = "hidden";
            field.name = this.field;
            this.el.form.append(field);
        }
        field.value = value ?? "";
    }

    _clearMany2OneValue() {
        if (!this.field || !this.el.form) {
            return;
        }
        const field = this.el.form.elements.namedItem(this.field);
        if (field && field !== this.el) {
            field.value = "";
        }
    }

    _showMenu() {
        this.menu.hidden = false;
        this.menu.classList.add("show");
        this.el.setAttribute("aria-expanded", "true");
    }

    _hideMenu() {
        this.menu.hidden = true;
        this.menu.classList.remove("show");
        this.el.setAttribute("aria-expanded", "false");
        this.el.removeAttribute("aria-activedescendant");
        this.items.forEach((item) => item.element.classList.remove("active"));
        this.activeIndex = -1;
    }
}

registry
    .category("public.interactions")
    .add("website_field_autocomplete", FieldAutocomplete);
