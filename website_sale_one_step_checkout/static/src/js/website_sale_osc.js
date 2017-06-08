(function() {
  'use strict';

  var website = openerp.website;

  function startTransaction(acquirer_id, form) {
    if (typeof openerp.website.prePaymenProcess === 'function') {
      // the transaction process should only start when the pre payment process is
      // finished
      openerp.website.prePaymenProcess(function(result) {
        openerp.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {}).then(function (data) {
          form.submit();
        });
      });
    } else {
      openerp.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {}).then(function (data) {
        form.submit();
      });
    }
  }

  function getPostAddressFields(elms, data) {
    elms.each(function(index) {
      data[$(this).attr('name')] = $(this).val();
    });

    return data;
  }

  function changeDelivery(carrierId) {
    openerp.jsonRpc('/shop/checkout/change_delivery', 'call', {'carrier_id': carrierId})
      .then(function (result) {
        if (result) {
          if (result.success) {
            if (result.order_total) {
              $('#order_total .oe_currency_value').text(result.order_total);
              $('#col-3 .js_payment input[name=amount]').val(result.order_total);
            }
            if (result.order_total_taxes) {
              $('#order_total_taxes .oe_currency_value').text(result.order_total_taxes);
            }
            if (result.order_subtotal) {
              $('#order_subtotal .oe_currency_value').text(result.order_subtotal);
            }
            if (result.order_total_delivery) {
              $('#order_delivery .oe_currency_value').text(result.order_total_delivery);
            }
          } else if (result.errors) {
            // ???
          }
        } else {
          // ???
          window.location.href = '/shop';
        }
      });
  }

  function validateAddress(ev) {
    var billingElms  = $('#osc_billing input, #osc_billing select')
      , shippingElms = $('#osc_shipping input, #osc_shipping select')
      , usedPayment  = $('input[name=acquirer]:checked').closest('li')
      , paymentElms  = $(usedPayment).find('div.payment-data input')
      , data         = {};

    data = getPostAddressFields(billingElms, data);

    if ($('#osc_billing select[name=shipping_id]').val() == '-1') {
      data = getPostAddressFields(shippingElms, data);
    }

    if (paymentElms.length) {
      data = getPostAddressFields(paymentElms, data);
      data['payment_data'] = true;
    }

    $('.oe_website_sale_osc .has-error').removeClass('has-error');

    openerp.jsonRpc('/shop/checkout/confirm_address/', 'call', data)
      .then(function (result) {
        if (result) {
          if (result.success) {
            var $form = $(ev.currentTarget).parents('form');
            var acquirer_id = $(ev.currentTarget).parents('div.oe_sale_acquirer_button').first().data('id');
            if (! acquirer_id) {
              return false;
            }
            startTransaction(acquirer_id, $form);
          } else if (result.errors) {
            for (var key in result.errors) {
              if ($('.oe_website_sale_osc input[name=' + key + ']').length > 0) {
                $('.oe_website_sale_osc input[name=' + key + ']').parent().addClass('has-error');
              } else if ($('.oe_website_sale_osc select[name=' + key + ']').length > 0) {
                $('.oe_website_sale_osc select[name=' + key + ']').parent().addClass('has-error');
              }
            }
          }
        } else {
          // ???
          window.location.href = '/shop';
        }
      });
  };

  website.dom_ready.done(function () {

    // when choosing an delivery carrier, update the total prices
    var $carrier = $('#delivery_carrier');
    $carrier.find('input[name="delivery_type"]').click(function (ev) {
      var carrierId = $(ev.currentTarget).val();
      changeDelivery(carrierId);
    });

    // when choosing an acquirer, display its order now button
    var $payment = $('#payment_method');
    $payment.on('click', 'input[name="acquirer"]',function(ev) {
      var payment_id = $(ev.currentTarget).val();
      $('div.oe_sale_acquirer_button[data-id]', '#col-3').addClass('hidden');
      $('div.oe_sale_acquirer_button[data-id="' + payment_id + '"]', '#col-3').removeClass('hidden');
    }).find('input[name="acquirer"]:checked').click();

    // terms and conditions
    var terms      = $('input[name=terms_conditions]')
      , formButton = $('.js_payment form button[type=submit]');
    if (terms.length) {
      // default state is deactivated checkbox and disabled submit button
      formButton.attr('disabled', 'disabled');
      terms.attr('checked', false);
      terms.click(function () {
        if (terms.is(':checked')) {
          formButton.attr('disabled', false);
        } else {
          formButton.attr('disabled', true);
        }
      });
    }

    //
    $carrier.find('input[checked="checked"]').trigger('click');

    // when clicking checkout submit button validate address data,
    // if all is fine form submit will be done in validate function because of
    // ajax call
    $('#col-3 .js_payment').on('click', 'form button[type=submit]', function(ev) {
      ev.preventDefault();
      ev.stopPropagation();
      validateAddress(ev);
      return false;
    });

    // Opens modal view when clicking on terms and condition link in
    // onestepcheckout, it loads terms and conditions page and render only wrap
    // container content in modal body
    $('.checkbox-modal-link').on('click', 'a', function(ev) {
      var elm   = $(ev.currentTarget)
        , title = elm.attr('title')
        , page  = elm.attr('data-page-id');

      $.get(page, function (data) {
        var modalBody = $(data).find('main .oe_structure').html();
        if (title) {
          $('#checkbox-modal .modal-header h4').text(title);
        }
        if (!modalBody) {
          modalBody = '<div class="container"><div class="col-md-12"><p>Informationen text</p></div></div>';
        }
        $('#checkbox-modal .modal-body').html(modalBody);
        $('#checkbox-modal').modal();
        return false;
      });
    });

  });

})();