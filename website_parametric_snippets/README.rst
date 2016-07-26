.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========================
website_parametric_snippets
===========================

This module adds extensions to view_view in order to render available 
to the programmer a new tag in qweb views: "t-ignore-branding".
Everything inside this tag will be ignored by the qweb evaluator, 
allowing the code to be evaluated on the fly.

The final result of this will be dynamic parameters in your widgets.


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



    ** Minimal working parametric snippet
        
        ** snippets.xml
        '''
        <template id="snippet_content_tmpl">
            <t t-set="variable" t-value="request.env['model'].model_function(myparameter)/>
            <div t-if="variable">
                <t t-esc="variable.name"/>   
                <!--supposing that model_function returns a record with an attribute "name" -->
            </div>
        </template>
        

        <template id="my_parametric_widget" inherit_id="website.snippets" 
             name="my_param_widget">
              <xpath expr="//div[@id='snippet_content']" position="inside">
                  <div>
                      <div class="oe_snippet_thumbnail">
                          <img class="oe_snippet_thumbnail_img" src="/module_name/image_path/img_name.png"/>
                          <span class="oe_snippet_thumbnail_title">Show parametric snippet</span>
                      </div>
                      <section class="oe_snippet_body jq_param_entry" >
                          <div class="parametricTemplate">
                              <!-- the template call code is injected via javascript 
                                   the class is parametricTemplate in order to 
                                   override odoo's normal behaviour 
                                   (no t tags allowed except for t-field) -->
                          </div>
                       </section>
                  </div>
              </xpath>
              <xpath expr="//div[@id='snippet_options']" position="inside">
                  <div data-snippet-option-id="param_entry" data-selector=".jq_parame_entry
                   data-selector-siblings="p, h1, h2, h3, blockquote, .well, .panel, .oe_share"
                   data-selector-children=".content">
                     <li class="dropdown-submenu"    data-required="false">
                         <a tabindex="-1" href="#">CHOOSE </a>
                         <t t-set="records" t-value="request.env['mymodel'].search([])"/>
                         <ul class="dropdown-menu">
                             <li t-foreach="record" t-as="record"  data-value="record.id" class="dropdown-submenu">
                                 <ul class="dropdown-menu">
                                     <li t-attf-data-value="param_#{record.id}">
                                         <a><t t-esc="record.name"</a>
                                     </li>
                                 </ul>
                             </li>
                         </ul>
                     </li>
                 </div>
              </xpath>
          </template>
        '''
      ** mymodule.js
        '''
        (function() {
            "use strict";
            var website = openerp.website;

            website.snippet.options["param_entry"]= openerp.website.snippet.Option.extend(
            {   
                select: function (event, np)
                {  
                    var selection = event.$next.first().attr('data-value').split("_");
                    var content = this.$target; 
                    content.attr('data-parameter_id', selection[0])
                           .attr('data-record_id', selection[1]);
                },
                start: function()
                {   
                    this.$target.find('.parametricTemplate').html("click here to select");
                },
                onFocus: function()
                {  
                    this.$target.find('.parametricTemplate').html("Select record to display from options");
                },
                clean_for_save: function() 
                {
                    this.$target.find('.parametricTemplate')
                        .empty()
                        .append(
                            jQuery('<t />')
                                .attr('t-call', 'my_module_name.snippet_content_tmpl')
                                .attr('t-ignore-branding', '1')
                                .append(
                                    jQuery('<t />')
                                       .attr('t-value', this.$target.attr('data-record_id'))
                                       .attr('t-set', 'record_id')
                                       .attr('t-ignore-branding', '1'),
                                     )
                               
                        );
                
                }

            });
        })();
        '''


    **Examples of modules that use this tag (will be updated)

        - website_snippet_blog_display_post
        - website_twitter_no_ext_links




#. go to ...
.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt

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

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* gfcapalbo <giovanni@therp.nl>  

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
