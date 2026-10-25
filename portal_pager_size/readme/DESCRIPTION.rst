This module adds a page size selector to portal pages in Odoo.

Users can choose how many records are displayed per page using a dropdown
integrated into the portal pager. The selected value is applied via a
``limit`` query parameter and affects pagination behavior accordingly.

Key features:

- Adds a page size selector to the portal pager
- Supports configurable limit options (e.g. 10, 20, 40, 80, 100)
