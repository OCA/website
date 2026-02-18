## Configuration

No additional configuration is required for this module. It automatically extends the functionality of the `website_whatsapp` module.

The module uses the existing WhatsApp configuration from the base `website_whatsapp` module. To configure WhatsApp settings:

1. Go to **Website > Configuration > Settings**
2. Scroll to the **WhatsApp** section
3. Configure the following fields:
   - **whatsapp_number**: The WhatsApp phone number (with country code) where messages will be sent
   - **whatsapp_text**: The default message text for non-product pages (homepage, contact, etc.)
   - **whatsapp_track_url**: Enable to append the current page URL to WhatsApp messages

Once configured, the module will automatically:
- Use dynamic product-specific messages on product pages
- Use the default `whatsapp_text` message on all other pages
- Append the page URL to messages when `whatsapp_track_url` is enabled
