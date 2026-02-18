# Design Document: website_whatsapp_dynamic_message

## Overview

The `website_whatsapp_dynamic_message` module extends the OCA `website_whatsapp` module
to provide context-aware WhatsApp messages. The module detects when a visitor is viewing
a product page and automatically generates a personalized message that includes the
product name. For all other pages (homepage, contact, about, etc.), the module uses the
default message configured in the website settings.

### Key Design Decisions

1. **Template-based approach**: Extend the existing `website_whatsapp.layout` template
   to modify message generation logic without duplicating code
2. **Context detection**: Use the QWeb rendering context to detect product pages by
   checking for the presence of a `product` variable
3. **Method override**: Override the `_get_track_url_message` method on the `website`
   model to inject dynamic message logic
4. **Zero configuration**: No additional configuration fields required; works
   immediately with existing `website_whatsapp` settings
5. **Translatable templates**: Use Odoo's translation system (`_()`) for the dynamic
   message template to support multilingual websites

## Architecture

### Module Structure

```
website_whatsapp_dynamic_message/
├── __init__.py
├── __manifest__.py
├── pyproject.toml
├── models/
│   ├── __init__.py
│   └── website.py
├── templates/
│   └── website.xml
├── tests/
│   ├── __init__.py
│   └── test_dynamic_message.py
├── i18n/
│   └── website_whatsapp_dynamic_message.pot
└── readme/
    ├── DESCRIPTION.md
    ├── CONFIGURE.md
    ├── USAGE.md
    └── CONTRIBUTORS.md
```

### Dependencies

- `website_whatsapp`: Base module providing WhatsApp button functionality
- `website_sale`: Provides product page context and product.template model access

### Integration Points

1. **Template inheritance**: Inherits `website_whatsapp.layout` template
2. **Model inheritance**: Extends `website` model to override message generation
3. **Context access**: Reads product information from QWeb rendering context

## Components and Interfaces

### Component 1: Website Model Extension

**File**: `models/website.py`

**Purpose**: Override message generation logic to provide context-aware messages

**Methods**:

```python
class Website(models.Model):
    _inherit = "website"

    def _get_dynamic_whatsapp_message(self, product=None):
        """
        Generate a dynamic WhatsApp message based on context.

        Args:
            product: product.template record or None

        Returns:
            str: The message text (not URL encoded)
        """
        # If product context exists, generate product-specific message
        # Otherwise, return the default configured message
        pass

    def _get_track_url_message(self, httprequest_full_path, product=None):
        """
        Override base method to support dynamic messages.

        Args:
            httprequest_full_path: The current page path
            product: product.template record or None

        Returns:
            str: URL-encoded message with optional track URL
        """
        # Get dynamic or default message
        # Apply URL encoding
        # Append track URL if enabled
        pass
```

**Key Logic**:

1. `_get_dynamic_whatsapp_message()`:

   - Check if `product` parameter is provided and is a valid record
   - If yes: Generate message using translatable template:
     `_("Hello, I'm interested in product %s, I would like more information") % product.name`
   - If no: Return `self.whatsapp_text` (default message)

2. `_get_track_url_message()`:
   - Accept optional `product` parameter (new)
   - Call `_get_dynamic_whatsapp_message(product)` to get base message
   - Apply URL encoding to the message
   - If `self.whatsapp_track_url` is enabled, append formatted URL
   - Return complete URL-encoded message

### Component 2: Template Extension

**File**: `templates/website.xml`

**Purpose**: Modify the WhatsApp button template to pass product context to message
generation

**Template Structure**:

```xml
<template id="layout" inherit_id="website_whatsapp.layout">
    <xpath expr="//t[@t-if='website.whatsapp_track_url']" position="replace">
        <!-- Detect product context -->
        <t t-set="current_product" t-value="product if product else None" />

        <!-- Generate message with product context -->
        <t t-if="website.whatsapp_track_url">
            <t
        t-set="extra_info"
        t-value="website._get_track_url_message(request.httprequest.full_path, current_product)"
      />
        </t>
    </xpath>

    <!-- Also handle non-track-url case -->
    <xpath expr="//t[@t-if='website.whatsapp_text']" position="replace">
        <t t-set="current_product" t-value="product if product else None" />
        <t t-if="not website.whatsapp_track_url">
            <t
        t-set="extra_info"
        t-value="website._get_dynamic_whatsapp_message(current_product)"
      />
        </t>
    </xpath>
</template>
```

**Key Logic**:

1. Detect if `product` variable exists in the rendering context
2. Pass product to message generation methods
3. Replace both the track URL and non-track URL message generation logic
4. Maintain backward compatibility by handling `None` product gracefully

### Component 3: Test Suite

**File**: `tests/test_dynamic_message.py`

**Purpose**: Verify dynamic message generation across different contexts

**Test Class Structure**:

```python
from odoo.tests import TransactionCase, tagged

@tagged("post_install", "-at_install")
class TestDynamicWhatsappMessage(TransactionCase):

    def setUp(self):
        # Create test website with whatsapp configuration
        # Create test product
        pass

    def test_product_page_dynamic_message(self):
        # Test: Product page generates dynamic message with product name
        pass

    def test_homepage_default_message(self):
        # Test: Homepage uses default configured message
        pass

    def test_special_characters_encoding(self):
        # Test: Product names with special chars are properly encoded
        pass

    def test_track_url_with_dynamic_message(self):
        # Test: Track URL appends correctly to dynamic message
        pass

    def test_missing_product_context(self):
        # Test: Gracefully handles None product
        pass

    def test_empty_default_message(self):
        # Test: Handles empty whatsapp_text configuration
        pass

    def test_unicode_product_name(self):
        # Test: Unicode characters in product names
        pass
```

## Data Models

### No New Models

This module does not introduce new database models. It extends the existing `website`
model from the `website` core module.

### Extended Model: website

**Inherited from**: `website` (core Odoo module)

**New/Modified Fields**: None (uses existing fields from `website_whatsapp`)

**New/Modified Methods**:

1. `_get_dynamic_whatsapp_message(product=None)` - NEW

   - Returns: `str` (plain text message)
   - Purpose: Generate context-aware message

2. `_get_track_url_message(httprequest_full_path, product=None)` - MODIFIED
   - Added parameter: `product` (optional)
   - Returns: `str` (URL-encoded message)
   - Purpose: Override base method to support dynamic messages

### Data Flow

```
Page Request
    ↓
QWeb Template Rendering (website.xml)
    ↓
Detect product context (product variable exists?)
    ↓
Call website._get_track_url_message(path, product)
    ↓
Call website._get_dynamic_whatsapp_message(product)
    ↓
Generate message (dynamic if product, default otherwise)
    ↓
Apply URL encoding
    ↓
Append track URL if enabled
    ↓
Render WhatsApp button with message
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid
executions of a system—essentially, a formal statement about what the system should do.
Properties serve as the bridge between human-readable specifications and
machine-verifiable correctness guarantees.

### Property 1: Product Name Inclusion in Dynamic Messages

_For any_ product.template record with a non-empty name, when generating a WhatsApp
message with that product as context, the resulting message should contain the product's
name.

**Validates: Requirements 1.1, 1.3, 4.1, 4.2**

### Property 2: URL Encoding for Special and Unicode Characters

_For any_ product name containing special characters (e.g., &, %, #, spaces) or Unicode
characters (e.g., é, ñ, 中文), the generated WhatsApp message should be properly
URL-encoded such that all characters are safe for URL transmission.

**Validates: Requirements 1.4, 5.1, 5.2, 5.3**

### Property 3: Track URL Integration with Dynamic Messages

_For any_ product page where `whatsapp_track_url` is enabled, the generated message
should contain both the dynamic product message and the formatted page URL.

**Validates: Requirements 1.5**

### Property 4: Default Message on Non-Product Pages

_For any_ page context without a product object, the generated WhatsApp message should
equal the configured `whatsapp_text` value from website settings.

**Validates: Requirements 2.2, 10.3**

### Property 5: Track URL Integration with Default Messages

_For any_ non-product page where `whatsapp_track_url` is enabled, the generated message
should contain both the default message and the formatted page URL.

**Validates: Requirements 2.3**

### Property 6: Base Module Functionality Preservation

_For any_ website configuration with `whatsapp_number` and `whatsapp_text` set, calling
the base module's message generation methods should produce valid WhatsApp URLs that
include the configured number and message.

**Validates: Requirements 3.1, 6.2**

### Property 7: Translation Support for Dynamic Messages

_For any_ language context, when generating a dynamic message for a product, the message
template (excluding the product name) should be translated to that language while
preserving the product name.

**Validates: Requirements 9.4**

## Error Handling

### Empty or Missing Configuration

**Scenario**: `whatsapp_text` is not configured (empty or False)

**Handling**:

- `_get_dynamic_whatsapp_message()` should return an empty string for non-product
  contexts
- For product contexts, should still generate the product-specific message
- Template should handle empty messages gracefully (button still renders if
  `whatsapp_number` is set)

**Validates: Requirements 3.2** (edge case)

### Missing Product Context

**Scenario**: Product page template is rendered but product variable is None or invalid

**Handling**:

- Check if product parameter is truthy and is a valid recordset
- If not valid, fall back to default message behavior
- Use defensive programming: `if product and product.id:`

**Validates: Requirements 4.3** (edge case)

### Special Characters in Product Names

**Scenario**: Product name contains characters that need URL encoding

**Handling**:

- Use `urllib.parse.quote()` or Odoo's URL encoding utilities
- Encode the entire message text, not just the product name
- Preserve Unicode characters while encoding special URL characters

**Validates: Requirements 1.4, 5.1, 5.2** (edge case)

### Invalid URL Paths

**Scenario**: `httprequest_full_path` contains query parameters or fragments

**Handling**:

- Use the existing base module logic that cleans URLs with `urlparse` and `urlunparse`
- Remove query parameters to avoid cluttering the WhatsApp message
- Maintain the base module's URL cleaning behavior

## Testing Strategy

### Dual Testing Approach

This module will use both unit tests and example-based tests to ensure comprehensive
coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Example tests**: Verify specific scenarios like homepage behavior and template
  structure

### Unit Test Coverage

The test suite (`tests/test_dynamic_message.py`) will include:

1. **Dynamic Message Generation Tests**:

   - Test that product names appear in messages (Property 1)
   - Test message format matches expected template (Requirement 1.2)
   - Test with various product names (short, long, with spaces)

2. **URL Encoding Tests**:

   - Test special characters: `&`, `%`, `#`, `?`, `=`, spaces (Property 2)
   - Test Unicode characters: accented letters, emoji, CJK characters (Property 2)
   - Test combined special and Unicode characters

3. **Track URL Tests**:

   - Test track URL with dynamic messages (Property 3)
   - Test track URL with default messages (Property 5)
   - Test track URL disabled (should not append URL)

4. **Context Detection Tests**:

   - Test product page context (Property 1)
   - Test non-product page context (Property 4)
   - Test missing/None product context (Error Handling)
   - Test invalid product recordset

5. **Backward Compatibility Tests**:

   - Test base module methods still work (Property 6)
   - Test with existing whatsapp_text configuration (Property 4)
   - Test with empty whatsapp_text (Error Handling)

6. **Translation Tests**:

   - Test message template translation (Property 7)
   - Test product name preservation in translated messages
   - Test with multiple languages (en_US, es_ES, fr_FR)

7. **Edge Cases**:
   - Empty default message (Requirement 3.2)
   - Missing product context (Requirement 4.3)
   - Product with empty name
   - Very long product names

### Test Configuration

- Use Odoo's `TransactionCase` for database-dependent tests
- Tag tests with `@tagged("post_install", "-at_install")`
- Each test should be independent and not rely on other tests
- Use `setUp()` to create common test data (website, products)
- Clean up test data in `tearDown()` if necessary

### Example Test Structure

```python
from odoo.tests import TransactionCase, tagged
from urllib.parse import unquote

@tagged("post_install", "-at_install")
class TestDynamicWhatsappMessage(TransactionCase):

    def setUp(self):
        super().setUp()
        self.website = self.env["website"].create({
            "name": "Test Website",
            "whatsapp_number": "1234567890",
            "whatsapp_text": "Hello, how can we help you?",
            "whatsapp_track_url": False,
        })
        self.product = self.env["product.template"].create({
            "name": "Test Product",
            "list_price": 100.0,
        })

    def test_dynamic_message_contains_product_name(self):
        """Test Property 1: Product name appears in dynamic message"""
        message = self.website._get_dynamic_whatsapp_message(self.product)
        self.assertIn(self.product.name, message)

    def test_special_characters_encoded(self):
        """Test Property 2: Special characters are URL encoded"""
        product = self.env["product.template"].create({
            "name": "Product & Service #1",
        })
        message = self.website._get_track_url_message("/shop", product)
        # Message should be URL encoded
        self.assertIn("%26", message)  # & encoded
        self.assertIn("%23", message)  # # encoded

    def test_default_message_without_product(self):
        """Test Property 4: Default message used without product context"""
        message = self.website._get_dynamic_whatsapp_message(None)
        self.assertEqual(message, self.website.whatsapp_text)

    # Additional tests...
```

### OCA Pre-commit Compliance

All code must pass OCA pre-commit hooks:

- **ruff**: Python linting and formatting
- **pylint-odoo**: Odoo-specific linting rules
- **prettier**: XML/JS/CSS formatting
- **eslint**: JavaScript linting (if applicable)

Run before committing:

```bash
pre-commit run --all-files
```
