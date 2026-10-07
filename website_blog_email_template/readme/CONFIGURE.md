This module does not require additional configuration after installation. It works automatically once installed.

## Installation

1. Go to the **Apps** menu
2. Remove the "Apps" filter if necessary
3. Search for "Website Blog Email Template"
4. Click **Install**

## Prerequisites

Make sure the following modules are installed:
* **Website Blog** (base blog module)

The system will automatically install the necessary dependencies during installation.

## Default Template

After installation, a default custom template is available:
* **Template Name**: "Blog: New Post Published (Custom Template)"
* **Location**: Settings > Technical > Email > Templates
* **Model**: Blog (blog.blog)

You can use this template as-is, customize it, or create new templates based on it.

## Permissions

The module uses the same access permissions as the base modules:
* Users with access to **Website** and **Blogs** can configure email templates for blogs
* Users with access to **Settings > Technical > Email > Templates** can create and edit email templates

No additional permission configuration is required.

## Template Configuration

**Template Requirements:**

1. **Model**: Must be set to "Blog" (blog.blog)
2. **Subject**: Can use `{{ object.name }}` for blog name
3. **Body**: HTML content with access to:
   - Blog object: `object.name`, `object.subtitle`
   - Post context: `ctx.get('blog_post')` for post information

**Recommended Template Structure:**

* Include a greeting
* Display blog name
* Show post title and subtitle
* Include a link to the post using `ctx.get('blog_post').website_url`
* Add a closing message

