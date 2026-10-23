To use this module, you need to:

1. **Configure the Country VAT Label (Backend):**
   * Go to **Contacts** > **Configuration** > **Countries**.
   * Search for and select the country you want to configure (e.g., *Brazil* or *Chile*).
   * In the form view, locate the **VAT Label** field and enter the local terminology (e.g., *CPF/CNPJ* or *RUT*).
   * Click **Save**.

   ![Configure Country VAT Label in Backend](static/description/country_form.png)

2. **Check the Website Checkout/Address Form (Frontend):**
   * Go to your **Website** shop.
   * Add any product to the cart and proceed to the **Checkout**.
   * On the **Billing/Shipping Address** form, select the country you configured in step 1.
   * You will notice that the standard generic **"VAT"** input field label dynamically changes to match the localized label you defined (e.g., *RUT* or *CPF/CNPJ*).

   ![Dynamic VAT Label during Checkout](static/description/website_checkout.png)