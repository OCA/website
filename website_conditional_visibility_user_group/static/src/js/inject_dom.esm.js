/** @odoo-module */
/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {session} from "@web/session";

document.addEventListener("DOMContentLoaded", () => {
    const htmlEl = document.documentElement;
    htmlEl.dataset.user_group = session.user_group;
});
