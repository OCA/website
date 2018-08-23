To configure this module, you need to:

#. Have *Administration / Settings* privileges.
#. Go to *Settings > Activate developer mode*.
#. Go to *Settings > Technical > Database Structure > Models*.
#. Search for the model you want to manage website form access for.
#. When you find it, it will have a *Website Forms* section where you can:

   * Allow the model to get forms, by checking *Allowed to use in forms*.
   * Give the model forms a better name in *Label for form action*.
   * Choose the field where to store custom fields data in *Field for custom
     form data*. If you leave this one empty and the model is a mail thread,
     a new message will be appended with that custom data.

#. In the *Fields* tab, there's a new column called *Blacklisted in web forms*.
   It's a security feature that forbids form submitters to write to those
   fields. When you create a new website form, all its model fields are
   automatically whitelisted for the sake of improving the UX. If you want to
   have higher control, come back here after creating the form and blacklist
   any fields you want, although that will only work for custom fields.
