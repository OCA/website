To configure the shown breadcrumbs, you need to:

1.  Enable developer mode.
2.  Go to Website Admin \> Configuration \> Menus.
3.  Remove the website grouping from the filter if it is set.
4.  Edit any menu there.

Keep in mind that:

- This module will try to match **exactly** the URL in the menu item
  with the one you are browsing.
- If it finds no match, breadcrumbs will not be shown.
- If it finds several matches, only the first one will be used.
- Using more than 1 submenu for the website top menu will probably make
  it unusable. In case you need that granularity, you will have to
  create a separate top menu for managing your breadcrumbs.
- Breadcrumbs use the menu name, **not the page name**, except for the
  top menu item, which will appear as *Home* and point to `/` unless you
  specify an URL for it.
