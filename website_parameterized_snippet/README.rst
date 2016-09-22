.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
Parameterized Snippets
===========================

This module adds extensions in order to render available 
to the programmer a new tag in qweb views: "t-ignore-branding".
Everything inside this tag will be ignored by the qweb evaluator, 
allowing the code to be evaluated on the fly.

The final result of this will be dynamic parameters in your widgets.
This would allow widgets to be defined as "Show the last 5 entries of
this model"  or "Show all the data that has an attribute corresponding
to the selected attibute". 
Widgets therefore will display parameter-dependant (1,2, or n parameters) 
information, and most importantly keep it updated on every pageload.


Usage
=====

Creating a Parametric Snippet:

    Create a normal snippet and in the snippet_body_section create a 
    div that will contain the parametric part of the snippet content.
    Identify this div with a specific class, such as "parametricTemplate".
    This div will be empty ( we will inject via JS  our template call code.)
 

    Create a template stanza with the content of your snippet.

    Create a snippet options entry with a data-snippet-option-id and 
    a data-selector option.

    Create The javascript to tie everything together, the JS extends
    the snippet options by identifying it by data-snippet-option-id 
    fetches the selected  options and on clean_for_save event injects
    a t-call in the 'parametricTempalate' div of our actual content with
    attribute  ('t-ignore-branding', '1') and append also t-sets of the 
    desired parameters with their values, also with the attribute
    ('t-ignore-branding, '1') appended.


    
Examples of modules that use this tag (will be updated)
=======================================================
website_snippet_blog_display_post <https://github.com/gfcapalbo/website/tree/8.0-website_snippet_blog_display_post>.
website_twitter_no_ext_links  <https://github.com/gfcapalbo/website/tree/8.0-website_twitter_no_ext_links> .


For further information, please visit:

* https://www.odoo.com/forum/help-1


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website_panam_oca/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/website_panam_oca/issues/new?body=module:%20website_parametric_snippets%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Thanks to Holger Brunn <hbrunn@therp.nl> for the parametric t tag idea.

Thanks to Laurent Mignon <laurent.mignon@acsone.eu> for extending also website.qweb.field.html to render 
t-call elements inserted by snippets using the parametic approach and stored on the related model itself. 


Contributors
------------

* Giovanni Francesco Capalbo <giovanni@therp.nl>  
* Holger Brunn <hbrunn@therp.nl>
* Laurent Mignon  <laurent.mignon@acsone.eu>

Do not contact contributors directly about help with questions or problems concerning this addon, but use the `community mailing list <mailto:community@mail.odoo.com>`_ or the `appropriate specialized mailinglist <https://odoo-community.org/groups>`_ for help, and the bug tracker linked in `Bug Tracker`_ above for technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
