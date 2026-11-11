import {registry} from "@web/core/registry";
import {Plugin} from "@html_editor/plugin";
import {BaseOptionComponent} from "@html_builder/core/utils";
import {BuilderAction} from "@html_builder/core/builder_action";

const COL_CLASSES = {
    1: "col-12",
    2: "col-md-6",
    3: "col-md-4",
    4: "col-md-3",
};

export class FormColumnsOption extends BaseOptionComponent {
    static template = "website_form_multi_column.FormColumnsOption";
    static selector = ".s_website_form";
}

function getColumnCount(formEl) {
    const value = parseInt(formEl.dataset.multiColumn, 10);
    return Number.isFinite(value) && value >= 1 && value <= 4 ? value : 1;
}

function ensureColumnWrappers(formEl, count) {
    const rowsEl = formEl.querySelector(".s_website_form_rows");
    const colClass = COL_CLASSES[count];
    const existing = [...rowsEl.querySelectorAll(":scope > .o_form_column")];
    while (existing.length > count) {
        existing.pop().remove();
    }
    while (existing.length < count) {
        const col = document.createElement("div");
        col.className = `o_form_column ${colClass}`;
        rowsEl.appendChild(col);
        existing.push(col);
    }
    for (const col of existing) {
        col.classList.remove("col-12", "col-md-6", "col-md-4", "col-md-3");
        col.classList.add(...colClass.split(" "));
    }
    return existing;
}

// Keep-then-fill: preserve prior column per field, clamp on shrink, default to col 0.
function redistributeFields(formEl, columnEls, fieldEls, oldCount, newCount) {
    for (const fieldEl of fieldEls) {
        const prev = parseInt(fieldEl.parentElement.dataset.columnIndex, 10);
        const target = Number.isFinite(prev) ? Math.min(prev, newCount - 1) : 0;
        columnEls[target].appendChild(fieldEl);
    }
}

export class SetColumnCountAction extends BuilderAction {
    static id = "setColumnCount";

    apply({editingElement: formEl, value}) {
        const newCount = parseInt(value, 10);
        const oldCount = getColumnCount(formEl);
        const rowsEl = formEl.querySelector(".s_website_form_rows");

        // Tag current wrappers so redistributeFields can read prior placement.
        for (const col of rowsEl.querySelectorAll(":scope > .o_form_column")) {
            const idx = [...rowsEl.children].indexOf(col);
            col.dataset.columnIndex = String(idx);
        }

        const fieldEls = [
            ...rowsEl.querySelectorAll(":scope > .s_website_form_field"),
            ...rowsEl.querySelectorAll(
                ":scope > .o_form_column > .s_website_form_field"
            ),
        ].filter(
            (el) =>
                !el.classList.contains("s_website_form_submit") &&
                !el.classList.contains("s_website_form_recaptcha") &&
                !el.classList.contains("s_website_form_dnone")
        );

        if (newCount === 1) {
            for (const el of fieldEls) {
                rowsEl.appendChild(el);
            }
            for (const col of rowsEl.querySelectorAll(":scope > .o_form_column")) {
                col.remove();
            }
            delete formEl.dataset.multiColumn;
            return;
        }

        const columnEls = ensureColumnWrappers(formEl, newCount);
        redistributeFields(formEl, columnEls, fieldEls, oldCount, newCount);

        // Submit / recaptcha / hidden fields stay after the columns.
        for (const tail of rowsEl.querySelectorAll(
            ":scope > .s_website_form_submit, :scope > .s_website_form_recaptcha, :scope > .s_website_form_dnone"
        )) {
            rowsEl.appendChild(tail);
        }
        formEl.dataset.multiColumn = String(newCount);
    }

    isApplied({editingElement: formEl, value}) {
        return getColumnCount(formEl) === parseInt(value, 10);
    }
}

export class FormColumnsOptionPlugin extends Plugin {
    static id = "formColumnsOption";
    resources = {
        builder_options: [FormColumnsOption],
        builder_actions: {SetColumnCountAction},
        dropzone_selector: [
            {
                selector: ".s_website_form_field",
                exclude: ".s_website_form_dnone",
                dropIn: ".o_form_column",
                dropNear: ".s_website_form_field",
                dropLockWithin: "form",
            },
        ],
        content_editable_selectors: [".s_website_form form .o_form_column"],
    };
}

registry
    .category("website-plugins")
    .add(FormColumnsOptionPlugin.id, FormColumnsOptionPlugin);
