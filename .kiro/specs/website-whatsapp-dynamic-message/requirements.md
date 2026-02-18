# Requirements Document

## Introduction

This document specifies the requirements for the `website_whatsapp_dynamic_message`
module, which extends the OCA `website_whatsapp` module to provide context-aware dynamic
WhatsApp messages. The module will generate different WhatsApp messages based on the
current page context, specifically customizing messages for product pages while
maintaining default behavior for other pages.

## Glossary

- **System**: The `website_whatsapp_dynamic_message` Odoo module
- **Base_Module**: The `website_whatsapp` module from OCA
- **Product_Page**: A web page displaying a product.template record
- **Homepage**: The main landing page of the website (/)
- **Default_Message**: The message configured in website settings (whatsapp_text field)
- **Dynamic_Message**: A context-specific message generated based on the current page
- **WhatsApp_Button**: The floating WhatsApp icon rendered on the website
- **Track_URL**: The feature from Base_Module that appends the current page URL to
  messages

## Requirements

### Requirement 1: Dynamic Message Generation for Product Pages

**User Story:** As a website visitor viewing a product, I want the WhatsApp message to
automatically include the product name, so that I can quickly inquire about that
specific product without typing it manually.

#### Acceptance Criteria

1. WHEN a visitor is on a Product_Page, THE System SHALL generate a Dynamic_Message
   containing the product name
2. WHEN a visitor is on a Product_Page, THE System SHALL format the Dynamic_Message as
   "Hello, I'm interested in product [Product Name], I would like more information"
3. WHEN a visitor clicks the WhatsApp_Button on a Product_Page, THE System SHALL use the
   Dynamic_Message instead of the Default_Message
4. WHEN a Product_Page has a product with special characters in the name, THE System
   SHALL properly encode the product name for URL transmission
5. WHERE Track_URL is enabled on a Product_Page, THE System SHALL append the page URL to
   the Dynamic_Message

### Requirement 2: Default Message Behavior for Non-Product Pages

**User Story:** As a website visitor on the homepage or other pages, I want the WhatsApp
message to use the configured default message, so that I receive appropriate context for
those pages.

#### Acceptance Criteria

1. WHEN a visitor is on the Homepage, THE System SHALL use the Default_Message
   configured in website settings
2. WHEN a visitor is on any page that is not a Product_Page, THE System SHALL use the
   Default_Message configured in website settings
3. WHERE Track_URL is enabled on non-product pages, THE System SHALL append the page URL
   to the Default_Message

### Requirement 3: Backward Compatibility with Base Module

**User Story:** As a system administrator, I want the module to maintain full
compatibility with the base website_whatsapp module, so that existing configurations
continue to work without modification.

#### Acceptance Criteria

1. WHEN the System is installed, THE System SHALL preserve all existing Base_Module
   functionality
2. WHEN the Default_Message is not configured, THE System SHALL handle empty messages
   gracefully
3. WHEN the Base_Module is updated, THE System SHALL continue to function without
   requiring code changes
4. THE System SHALL use the same configuration fields from Base_Module (whatsapp_number,
   whatsapp_text, whatsapp_track_url)
5. THE System SHALL inherit and extend the Base_Module template without replacing it

### Requirement 4: Product Context Detection

**User Story:** As a developer, I want the system to accurately detect when a user is
viewing a product page, so that dynamic messages are generated only in the appropriate
context.

#### Acceptance Criteria

1. WHEN rendering a page, THE System SHALL determine if the current page is a
   Product_Page
2. WHEN a Product_Page is detected, THE System SHALL extract the product.template record
   from the page context
3. IF a Product_Page is detected but no product record is available, THEN THE System
   SHALL fall back to the Default_Message
4. THE System SHALL detect Product_Pages based on the presence of a product object in
   the rendering context

### Requirement 5: URL Encoding and Special Character Handling

**User Story:** As a website visitor, I want product names with special characters to be
transmitted correctly in WhatsApp messages, so that the message displays properly in
WhatsApp.

#### Acceptance Criteria

1. WHEN a product name contains special characters, THE System SHALL encode them for URL
   transmission
2. WHEN a product name contains Unicode characters, THE System SHALL preserve them
   correctly in the WhatsApp message
3. THE System SHALL use proper URL encoding for the entire message text
4. WHEN combining Dynamic_Message with Track_URL, THE System SHALL maintain proper
   encoding for both components

### Requirement 6: Template Inheritance and Extension

**User Story:** As a developer, I want the module to properly extend the base template,
so that the WhatsApp button rendering is modified without duplicating code.

#### Acceptance Criteria

1. THE System SHALL inherit the Base_Module template (website_whatsapp.layout)
2. THE System SHALL override the message generation logic while preserving the button
   rendering
3. THE System SHALL not duplicate template code from Base_Module
4. WHEN the Base_Module template changes, THE System SHALL automatically inherit those
   changes

### Requirement 7: Testing and Quality Assurance

**User Story:** As a developer, I want comprehensive automated tests, so that the
module's functionality is verified and regressions are prevented.

#### Acceptance Criteria

1. THE System SHALL include unit tests for message generation on Product_Pages
2. THE System SHALL include unit tests for Default_Message usage on non-product pages
3. THE System SHALL include tests for URL encoding with special characters
4. THE System SHALL include tests for Track_URL integration with dynamic messages
5. THE System SHALL include tests for graceful handling of missing product context
6. THE System SHALL pass all OCA pre-commit hooks (ruff, pylint-odoo, prettier, eslint)

### Requirement 8: OCA Module Standards Compliance

**User Story:** As an OCA contributor, I want the module to follow all OCA standards and
conventions, so that it can be accepted into the OCA repository.

#### Acceptance Criteria

1. THE System SHALL follow OCA module structure with readme/, models/, templates/,
   tests/, i18n/ directories
2. THE System SHALL include README fragments (DESCRIPTION.md, CONFIGURE.md, USAGE.md,
   CONTRIBUTORS.md)
3. THE System SHALL use AGPL-3 license
4. THE System SHALL declare version as 17.0.1.0.0
5. THE System SHALL list dependencies as ["website_whatsapp", "website_sale"]
6. THE System SHALL include pyproject.toml file
7. THE System SHALL include proper copyright headers in all Python files
8. THE System SHALL include translation template (.pot file)
9. THE System SHALL declare assets properly in **manifest**.py if JavaScript or CSS is
   added
10. THE System SHALL include Christopher Ormaza <chris.ormaza@gmail.com> and OCA as
    authors

### Requirement 9: Internationalization Support

**User Story:** As a multilingual website administrator, I want the dynamic message
template to be translatable, so that visitors see messages in their preferred language.

#### Acceptance Criteria

1. THE System SHALL make the Dynamic_Message template translatable
2. THE System SHALL generate translation keys for all user-facing text
3. THE System SHALL include a .pot translation template file
4. WHEN a visitor views a Product_Page in a different language, THE System SHALL use the
   translated message template with the product name

### Requirement 10: Module Installation and Configuration

**User Story:** As a system administrator, I want to install the module without
additional configuration, so that it works immediately with existing website_whatsapp
settings.

#### Acceptance Criteria

1. WHEN the System is installed, THE System SHALL automatically extend the Base_Module
   functionality
2. THE System SHALL not require additional configuration fields beyond those in
   Base_Module
3. WHEN the System is installed on a website with existing whatsapp_text configuration,
   THE System SHALL use that configuration for non-product pages
4. THE System SHALL be installable on any Odoo 17.0 instance with website_whatsapp and
   website_sale modules
