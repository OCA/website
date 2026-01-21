This module enhances the blog management capabilities in Odoo by adding professional features for better content management.

Features
--------

* **Visits Display**: Show visit counts in list, form, and kanban views
* **Backend Form Access**: Quick access button (gear icon) in list view to open post form in backend
* **Professional Editing**: Content tab with HTML editor supporting code view toggle
* **Enhanced Views**: Improved form, tree, and kanban views with visit information
* **Search Filters**: Filter posts with no visits

Usage
-----

After installing this module:

1. Navigate to **Website > Content > Blog Posts**
2. View visit counts in the list view (visits column)
3. Click the gear icon button next to a post name to open it in backend form view
4. Use the enhanced form view to edit posts with HTML/code toggle in the Content tab
5. Filter posts with no visits using the search filter
6. View visit counts in kanban cards

Technical Details
-----------------

* Extends `blog.post` model with method `action_open_backend_form()` to open backend form view
* Inherits and enhances existing views from `website_blog`:
  * Form view: Adds statistics section with visits and Content tab with HTML editor
  * Tree view: Adds visits column, post_date column, and backend form button
  * Search view: Adds "No Visits" filter
  * Kanban view: Displays visit count in cards
