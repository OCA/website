This module allows you to schedule blog posts for automatic publication at a specific date and time.

Features
--------

* **Scheduled Publication Date**: Add a datetime field to schedule when posts should be published
* **Quick Publish Button**: One-click immediate publication from the form view
* **Schedule Wizard**: User-friendly wizard to set the publication date
* **Visual Feedback**: Information banner displays scheduled date on the form
* **Smart Publication Logic**: Automatically prevents immediate publication if a future date is set
* **Automatic Cron Job**: Runs every hour to publish scheduled posts
* **Notification System**: Sends notifications to blog followers when posts are published
* **Search Filters**: Filter and group posts by publication or scheduled dates

Technical Details
-----------------

* Extends ``blog.post`` model with scheduling fields and methods
* Includes a transient model ``blog.post.schedule.date`` for the scheduling wizard
* Inherits and enhances form and search views from ``website_blog``
* The cron job uses ``_publish_scheduled_posts()`` method to process scheduled posts
* Handles edge cases like setting past dates, clearing scheduled dates, and multiple record writes
