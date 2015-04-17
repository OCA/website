(function($) {
    "use strict";

    $(document).ready(function() {

            $('form').submit(function (e) {

                if($('#bases-legales').length != 0) {

                    if($('#bases-legales').is(':checked')) {

                    } else {
                        e.preventDefault();
                        alert("Por favor, antes de continuar, debes leer y aceptar las bases legales");
                    }

                }

            });

    });

})(jQuery);