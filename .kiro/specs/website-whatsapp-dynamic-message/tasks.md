# Implementation Plan: website_whatsapp_dynamic_message

## Overview

This implementation plan breaks down the development of the
`website_whatsapp_dynamic_message` Odoo module into discrete, incremental tasks. Each
task builds on previous work, starting with module structure, then core functionality,
templates, tests, and finally documentation. The module extends `website_whatsapp` to
provide context-aware WhatsApp messages on product pages.

## Tasks

- [x] 1. Set up module structure and manifest

  - Create module directory structure (models/, templates/, tests/, i18n/, readme/)
  - Create `__init__.py` files for Python package structure
  - Create `__manifest__.py` with proper metadata, dependencies, and data files
  - Create `pyproject.toml` for OCA tooling configuration
  - Add copyright headers to all Python files
  - _Requirements: 8.1, 8.3, 8.4, 8.5, 8.6, 8.7, 8.10_

- [x] 2. Implement website model extension

  - [x] 2.1 Create models/website.py with Website model inheritance

    - Inherit `website` model
    - Implement `_get_dynamic_whatsapp_message(product=None)` method
    - Handle product context: generate dynamic message if product exists
    - Handle non-product context: return default `whatsapp_text`
    - Use translatable string for dynamic message template
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 9.1_

  - [x] 2.2 Write unit tests for dynamic message generation

    - Test dynamic message contains product name (Property 1)
    - Test message format matches template (Requirement 1.2)
    - Test default message returned without product context (Property 4)
    - Test empty default message handling (Requirement 3.2)
    - _Requirements: 1.1, 1.2, 2.2, 3.2_

  - [x] 2.3 Implement URL encoding and track URL support

    - Override `_get_track_url_message(httprequest_full_path, product=None)` method
    - Call `_get_dynamic_whatsapp_message(product)` to get base message
    - Apply proper URL encoding to message text
    - Append track URL if `whatsapp_track_url` is enabled
    - Maintain base module's URL cleaning logic
    - _Requirements: 1.4, 1.5, 2.3, 5.1, 5.2, 5.3_

  - [x] 2.4 Write unit tests for URL encoding and track URL
    - Test special character encoding (Property 2)
    - Test Unicode character encoding (Property 2)
    - Test track URL with dynamic message (Property 3)
    - Test track URL with default message (Property 5)
    - Test track URL disabled
    - _Requirements: 1.4, 1.5, 2.3, 5.1, 5.2, 5.3_

- [x] 3. Checkpoint - Ensure model tests pass

  - Run tests:
    `odoo-bin -c odoo.conf -d test_db -i website_whatsapp_dynamic_message --test-tags=website_whatsapp_dynamic_message --stop-after-init`
  - Verify all model-level tests pass
  - Ask the user if questions arise

- [x] 4. Implement template extension

  - [x] 4.1 Create templates/website.xml with template inheritance

    - Inherit `website_whatsapp.layout` template
    - Detect product context: check if `product` variable exists in QWeb context
    - Replace message generation logic to pass product context
    - Handle both track URL enabled and disabled cases
    - Maintain backward compatibility with base template structure
    - _Requirements: 1.3, 3.5, 4.1, 4.2, 4.4, 6.1, 6.2_

  - [x] 4.2 Write integration tests for template rendering
    - Test product context detection (Property 1)
    - Test message generation called with product parameter
    - Test base module button rendering preserved (Property 6)
    - Test missing product context fallback (Requirement 4.3)
    - _Requirements: 1.3, 3.1, 4.1, 4.2, 4.3, 6.2_

- [x] 5. Implement translation support

  - [x] 5.1 Generate translation template file

    - Create i18n/website_whatsapp_dynamic_message.pot
    - Extract translatable strings from Python code and templates
    - Include dynamic message template string
    - _Requirements: 8.8, 9.2, 9.3_

  - [x] 5.2 Write unit tests for translation support
    - Test message template is translatable (Property 7)
    - Test product name preserved in translated messages (Property 7)
    - Test with multiple language contexts (en_US, es_ES)
    - _Requirements: 9.1, 9.4_

- [x] 6. Checkpoint - Ensure all tests pass

  - Run full test suite:
    `odoo-bin -c odoo.conf -d test_db -i website_whatsapp_dynamic_message --test-tags=website_whatsapp_dynamic_message --stop-after-init`
  - Verify all tests pass (model, template, translation)
  - Run OCA pre-commit hooks: `pre-commit run --all-files`
  - Fix any linting or formatting issues
  - Ask the user if questions arise

- [x] 7. Create README documentation

  - [x] 7.1 Create readme/DESCRIPTION.md

    - Describe module purpose and functionality
    - Explain dynamic message generation for product pages
    - Mention backward compatibility with website_whatsapp
    - _Requirements: 8.2_

  - [x] 7.2 Create readme/CONFIGURE.md

    - Explain that no additional configuration is needed
    - Reference website_whatsapp configuration (Website > Configuration > Settings)
    - Mention whatsapp_number, whatsapp_text, whatsapp_track_url fields
    - _Requirements: 8.2, 10.2_

  - [x] 7.3 Create readme/USAGE.md

    - Explain behavior on product pages (dynamic message)
    - Explain behavior on other pages (default message)
    - Provide example messages
    - Mention translation support
    - _Requirements: 8.2_

  - [x] 7.4 Create readme/CONTRIBUTORS.md

    - Add Christopher Ormaza <chris.ormaza@gmail.com>
    - Add OCA as contributor
    - _Requirements: 8.2, 8.10_

  - [x] 7.5 Generate README.rst from fragments
    - Run `oca-gen-addon-readme` to generate README.rst
    - Verify generated README is complete and properly formatted
    - _Requirements: 8.2_

- [x] 8. Final validation and cleanup

  - [x] 8.1 Run complete test suite

    - Install module in test database
    - Run all tests with coverage
    - Verify no test failures
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 8.2 Run OCA pre-commit hooks

    - Execute `pre-commit run --all-files`
    - Fix any ruff, pylint-odoo, prettier, or eslint issues
    - Verify all hooks pass
    - _Requirements: 7.6_

  - [x] 8.3 Verify module installability

    - Test installation on clean Odoo 17.0 instance
    - Verify dependencies (website_whatsapp, website_sale) are available
    - Test module upgrade scenario
    - _Requirements: 10.4_

  - [x] 8.4 Manual testing checklist
    - Test on product page: verify dynamic message with product name
    - Test on homepage: verify default message
    - Test with track URL enabled: verify URL appended
    - Test with special characters in product name
    - Test with empty default message configuration
    - Test translation: change language and verify message template translated
    - _Requirements: 1.1, 1.2, 1.5, 2.1, 3.2, 9.4_

- [x] 9. Final checkpoint - Module complete
  - All tests pass
  - All OCA pre-commit hooks pass
  - Documentation complete
  - Module installable and functional
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional test-related sub-tasks that can be skipped for
  faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and early error detection
- The implementation follows OCA standards and best practices
- All code must be written in English
- Python code must include proper copyright headers
- Translation support is built-in from the start
