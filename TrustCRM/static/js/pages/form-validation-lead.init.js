/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Form validation Js File
*/

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();



var intTel = function () {

    var input = document.querySelector("#phone"),
    input2 = document.querySelector("#phone2"),
    errorMsg = document.querySelector("#error-msg"),
    validMsg = document.querySelector("#valid-msg"),
    errorMsg2 = document.querySelector("#error-msg2"),
    validMsg2 = document.querySelector("#valid-msg2");

    // here, the index maps to the error code returned from getValidationError - see readme
    var errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];

    var reset = function ($input, $errorMsg, $validMsg) {
        $input.classList.remove("error");
        $input.classList.remove("error");
        $errorMsg.innerHTML = "";
        $errorMsg.classList.add("hide");
        $validMsg.classList.add("hide");

    };
    var blur = function ($input, $errorMsg, $validMsg, $iti) {


        $input.addEventListener('blur', function () {
            reset($input, $errorMsg, $validMsg);
            if ($input.value.trim()) {
                if ($iti.isValidNumber()) {
                    $validMsg.classList.remove("hide");
                } else {
                    $input.classList.add("error");
                    var errorCode = iti.getValidationError();
                    $errorMsg.innerHTML = errorMap[errorCode];
                    $errorMsg.classList.remove("hide");

                }
            }
        });
    }

    var iti = window.intlTelInput(input, {
        // any initialisation o,ptions go here
        //nationalMode: true,
        initialCountry: "auto",
        geoIpLookup: function (callback) {
            $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
                var countryCode = (resp && resp.country) ? resp.country : "us";
                callback(countryCode);
            });
        },
        placeholderNumberType: 'MOBILE',
        utilsScript: "assets/js/pages/utils.init.js?1638200991544"
    });

    // on blur: validate
    blur(input, errorMsg, validMsg, iti);
    // on keyup / change flag: reset
    input.addEventListener('change', reset(input, errorMsg, validMsg));
    input.addEventListener('keyup', reset(input, errorMsg, validMsg));


    var iti2 = window.intlTelInput(input2, {
        initialCountry: "auto",
        geoIpLookup: function (callback) {
            $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
                var countryCode = (resp && resp.country) ? resp.country : "us";
                callback(countryCode);
            });
        },

        placeholderNumberType: 'MOBILE',

        utilsScript: "assets/js/pages/utils.init.js?1638200991544"
    });


    // on blur: validate
    blur(input2, errorMsg2, validMsg2, iti2);
    // on keyup / change flag: reset
    input.addEventListener('change', reset(input2, errorMsg2, validMsg2));
    input.addEventListener('keyup', reset(input2, errorMsg2, validMsg2));
    // on blur: validate

}

intTel();