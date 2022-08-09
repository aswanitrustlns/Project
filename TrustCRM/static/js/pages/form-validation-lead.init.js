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

            form.addEventListener('input', function(event) {
                const formData = new FormData(form);
                const name=formData.get('name')
                const age = formData.get('age');
                const is_agree=formData.get('email_agree');
                const mobile=formData.get('mobile')
                const email1=formData.get('email1');
                const email2=formData.get('email2');
                if(name){
                    var regName = /^[a-zA-Z]+ [a-zA-Z]+$/;
                    
                    if(!regName.test(name)){
                        // alert('Please enter your full name (first & last name).');
                        // document.getElementById('fullname').focus();
                        console.log("Invalid name")
                        $("#valid_name").show();
                        
                        
                    }else{
                        console.log("valid name")
                        $("#valid_name").hide();
                    }
                }
                if(email1 || email2){
                    $("#email_unav").attr('required',false);
                }
                if(mobile){
                    $("#invalid_mobile").hide()
                }
                if(age){
                    if(age>18){
                        $("#invalid_age").hide();
                        $("#age").prop('required',false);
                        
                    }
                    else{
                        $("#invalid_age").show();
                        $("#age").attr('required','required');                 
                        
                    }

                }
                
                if(is_agree=="on"){
                    console.log("agree check")
                    $('#email1').attr('readonly', true);
                    $('#email2').attr('readonly', true);
                    $("#email_agree").hide();
                    if(!mobile){
                        $("#invalid_mobile").show()

                        $("#phone").attr('required','required');

                    }
                   
                }
                else{
                    console.log("agree check else")
                    $('#email1').attr('readonly', false);
                    $('#email2').attr('readonly', false);
                    $("#email_agree").hide();
                    $("#invalid_mobile").hide()
                    $("#phone").prop('required',false);
                }
              
                // Validate the pattern again. 
                
              
                // This will either be true or false based on if the values are the same or not.
                
              });     




            form.addEventListener('submit', function (event) {
                const formData = new FormData(form);
                const name=formData.get('name')
                const email1=formData.get('email1');
                const email2=formData.get('email2');
                const is_agree=formData.get('email_agree');
                const mobile=formData.get('mobile')
                console.log(mobile)
                if(!name){
                    $("#fullname").attr('required','required');
                }
                if(!email1&&!email2){
                    console.log("no email")
                    if(is_agree=="on"){
                        console.log("agree check")
                        $('#email1').attr('readonly', true);
                        $('#email2').attr('readonly', true);
                        $("#email_agree").hide();
                        if(!mobile){
                            console.log("No mobile")
                            $("#phone").attr('required','required');
                            $("#invalid_mobile").show()
                        }
                        else{
                            console.log("mobile is present")
                            $("#invalid_mobile").hide()
                        }
                    }
                     else{
                        $("#invalid_mobile").hide()
                        $("#email_agree").show();
                        $("#email_unav").attr('required','required');
                     }
                }
                if (form.checkValidity() === false ) {
                    console.log("validity check")
                    event.preventDefault();
                    event.stopPropagation();
                }
               
                    form.classList.add('was-validated');
               
             
                
            }, false);
        });
    }, false);
})();



var intTel = function () {

    var input = document.querySelector("#phone");
    var input2 = document.querySelector("#phone2");
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
        // separateDialCode: true,
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

    input.addEventListener('input', function() { 
        var mobileCountryName = iti.getSelectedCountryData().dialCode; 
        document.getElementById('mobile_country').value = mobileCountryName;   
        console.log("Country NAme"+mobileCountryName)
       
      });
      input2.addEventListener('input', function() {     
        var teleCountryName=iti2.getSelectedCountryData().dialCode;           
        document.getElementById('tel_country').value = teleCountryName;  
        console.log("Country NAme"+teleCountryName)
      });

      $('#reset').click(function(){
        $(".invalid-feedback").hide();
        $("#lead_form")[0].reset();
        

      })

}


intTel();