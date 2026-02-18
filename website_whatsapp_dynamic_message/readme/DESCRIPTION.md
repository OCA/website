This module extends the OCA `website_whatsapp` module to provide context-aware dynamic WhatsApp messages for product pages.

When visitors browse your website, the WhatsApp button automatically adapts its message based on the page they're viewing:

- **Product pages**: Generates a personalized message that includes the product name, making it easy for customers to inquire about specific products
- **Other pages** (homepage, contact, about, etc.): Uses the default message configured in your website settings

The module seamlessly integrates with the existing `website_whatsapp` configuration and requires no additional setup. It maintains full backward compatibility with the base module, preserving all existing functionality including URL tracking and custom message configuration.

**Key Features:**

- Automatic product name inclusion in WhatsApp messages on product pages
- Proper handling of special characters and Unicode in product names
- Support for URL tracking on both product and non-product pages
- Translatable message templates for multilingual websites
- Zero configuration required - works immediately after installation
