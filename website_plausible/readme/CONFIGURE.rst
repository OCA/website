To configure a website to be integrated with Plausible, you need to:

#. Go to *Website > Configuration > Settings*.
#. Enable 'Plausible Analytics'.
#. Fill in your 'Shared Link Auth'.

In case you host Plausible on your own server, you need to:

#. Activate the developer mode (in Settings)
#. Go to *Settings > Technical > System Parameters*.
#. Create the following parameter: key 'website.plausible_script' and value 'https://<your_plausible_domain.com>/js/script.js'
#. Create the following parameter: key 'website.plausible_server' and value 'https://<your_plausible_domain.com>'
