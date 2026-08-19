/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {session} from "@web/session";

// Transfer the session's user group as an HTML element attribute so that the
// conditional visibility CSS selectors can be based on it. It's done at import
// time (and not on DOMContentLoaded) so the attribute is already set when
// website's `unhideConditionalElements()` injects the visibility rules.
document.documentElement.dataset.user_group = session.user_group;
