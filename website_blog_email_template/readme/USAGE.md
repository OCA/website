This guide explains how to use the Website Blog Email Template module to configure custom email notifications for new blog posts.

## Configure a Custom Email Template for a Blog

**Step 1: Access Blog Settings**

1. Go to the **Website** module
2. Navigate to **Blogs** > **Blogs**
3. Select the blog you want to configure
4. Open the blog form view

**Step 2: Select or Create Email Template**

1. In the blog form, locate the **Email Template for New Posts** field
2. You have two options:
   * **Option A**: Select an existing template from the dropdown
   * **Option B**: Create a new template (click the search icon and then "Create")

**Step 3: Create a New Template (if needed)**

1. Click on the **Email Template for New Posts** field
2. Click the search icon (magnifying glass)
3. Click **Create** button
4. Fill in the template form:
   * **Name**: Give your template a descriptive name (e.g., "Blog Post Notification - Marketing")
   * **Model**: Should be set to "Blog" (blog.blog)
   * **Subject**: Email subject line (e.g., "New post: {{ object.name }}")
   * **Body**: HTML content of the email
5. Save the template
6. Select it in the blog's **Email Template for New Posts** field

**Step 4: Save the Blog Configuration**

1. Save the blog form
2. The custom template will now be used when new posts are published

## Using Context Variables in Templates

When creating or editing a template, you can use the following context variables:

**Blog Information:**
* `{{ object.name }}` - Blog name
* `{{ object.subtitle }}` - Blog subtitle

**Post Information (via context):**
* `{{ ctx.get('blog_post').name }}` - Post title
* `{{ ctx.get('blog_post').subtitle }}` - Post subtitle
* `{{ ctx.get('blog_post').author_name }}` - Author name
* `{{ ctx.get('blog_post').website_url }}` - Direct link to the post
* `{{ ctx.get('blog_post_id') }}` - Post ID

**Example Template Body:**

```html
<div style="margin: 0px; padding: 0px; font-size: 13px;">
    <p>Hello,<br/><br/>
    A new post has been published on the <strong>{{ object.name }}</strong> blog:<br/><br/>
    <strong>{{ ctx.get('blog_post').name }}</strong><br/><br/>
    <a href="{{ ctx.get('blog_post').website_url }}">Read the full post</a>
    </p>
</div>
```

## Automatic Behavior

**Template Selection Logic**

When a new blog post is published:
1. The system checks if the blog has a custom template configured
2. **If a template is configured**: Uses `message_post_with_template()` with the custom template
3. **If no template is configured**: Uses the default template (`website_blog.blog_post_template_new_post`)

**Notification Recipients**

* Only blog followers receive the notification
* The notification uses the subtype "Published Post" (mt_blog_blog_published)
* Email layout uses "mail.mail_notification_light" for custom templates

## Usage Examples

**Example 1: Simple Custom Template**

1. Create a blog "Company News"
2. Create a template with subject: "New article on {{ object.name }}"
3. Body includes post title and link
4. Configure the template in the blog
5. When posts are published, followers receive the custom email

**Example 2: Branded Template**

1. Create a blog "Product Updates"
2. Create a template matching your company branding
3. Include company logo, colors, and specific formatting
4. Add additional information like author bio or related posts
5. Configure in the blog settings

**Example 3: Multi-language Support**

1. Create different templates for different languages
2. Configure language-specific templates per blog
3. Templates can use language-specific formatting and content

## Tips

* Test your template before publishing posts by using the "Send Test Email" feature in the template
* Use the default template as a reference when creating custom templates
* Include the post link (`ctx.get('blog_post').website_url`) to make it easy for readers to access the content
* Consider your email client compatibility when designing HTML templates
* The template is rendered with the blog as `object`, so use `object.name` for blog name
* Post information is available through context, so use `ctx.get('blog_post')` to access post data

