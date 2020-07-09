v1.0.11
=======
* Fix help page 404
* Fix portal reply 500

v1.0.10
=======
* Fix issue with translations caused by the change of field category to category_id in version 12 to match naming conventions

v1.0.9
======
* Prevent direct help page access

v1.0.8
======
* Fix links in new ticket in category email

v1.0.7
======
* Portal user reply fix

v1.0.6
======
* Add ability for clients to add attachments in there replies from the website interface

v1.0.5
======
* Custoemr replies should always send off email notification to followers
* Customer replies made via website interface should be added to chatter as the user instead of odoobot

v1.0.4
======
* Chinese(Traditional) translation courtesy of "UniPiece Limited, Simon Chaung <simon@unipiece.com.tw>"

v1.0.3
======
* Adds ticket compose email template that uses user email (same as version 11), default is still company as from address.

v1.0.2
======
* Add dropbox as sub category custom field type

v1.0.1
======
* Fix issue with not being able to submit tickets whose category has multiple assigned users

v1.0.0
======
* Port to version 12
* Revamp settings display
* Removal of depricated contact extra ticket access feature (use departments)
* Removal of depricated SLA category times (use rules, it can do combination categories, sub categories and priority based SLAs)
* Include SLA in new ticket email
* Close comment templates and support for html
* Various internal changes to standardise naming and coding conventions