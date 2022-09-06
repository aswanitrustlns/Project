//update Inputrange
function updateInput($this,$id) {  
    var val =$this.value; 
    //console.log(val);
   $('#'+$id).html(val);
    //document.getelementbyId($id).html(val);
   
}  

//on edit Mode

function onloadEditmode($id,$class) {
    $('#'+$id).find('select').attr("disabled", "disabled");
    $('#'+$id).find('input').attr("disabled", "disabled");
    $('#'+$id).removeClass($class);
}
$(document).ready(function () {

    
    onloadEditmode('formtypeleads','editable-enabled');
});


//adddisbled('#formtypeleads','editable-enabled');

//$('#formtypeleads
//Edit Butt
function updateEditmode($elm,$text1,$text2,$id,$class) {  
    var $this=$('#'+$id);
    //val x=if ($(this).hasAttr("name"))
    if($this.find('select').attr("disabled") ){
        $this.find('select').removeAttr( "disabled" );
        $this.find('input').removeAttr( "disabled" );
        $this.addClass($class);
        $($elm).text($text2);

    }
    else{
        $this.find('select').attr("disabled", "disabled");
        $this.find('input').attr("disabled", "disabled");
        $this.removeClass($class);
        $($elm).text($text1);
    }
   
}  



//intTel
var intTel = function () {

    var input = document.querySelector("#phone"),
    input2 = document.querySelector("#phone2"),
    errorMsg = document.querySelector("#error-msg"),
    validMsg = document.querySelector("#valid-msg"),
    errorMsg2 = document.querySelector("#error-msg2"),
    validMsg2 = document.querySelector("#valid-msg2");

    // here, the index maps to the error code returned from getValidationError - see readme
    var errorMap = ["Invalid number","Invalid country code", "Too short", "Too long", "Invalid number"];

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


//flatpicker
flatpickr('#datepicker-timepicker', {
    enableTime: true,
    noCalendar: true,
    dateFormat: "h:i:K",
    defaultDate: new Date()
});

flatpickr('#datepicker', {
    //inline: true,
    dateFormat: "M-d-Y",
    defaultDate: new Date()
});

flatpickr('#datepicker-timepicker-meeting', {
    enableTime: true,
    noCalendar: true,
    dateFormat: "h:i:K",
    defaultDate: new Date()
});

flatpickr('#datepicker-meeting', {
    //inline: true,
    dateFormat: "M-d-Y",
    defaultDate: new Date()
});


//TR



//Scroll function update and reset btn
var scroll= function(el){
    $(window).scroll(function(e){ 
        var $el= $(el); 
        var isPositionFixed = ($el.css('position') == 'fixed');
        if ($(this).scrollTop() > 200 && !isPositionFixed){ 
          $el.css({'position': 'fixed', 'top': '55px', 'left': '0px', 'right': '20px',  'transform': 'translateX(0%)', 'z-index': '1053', 'margin-left': '250px'  });
         
          //$el.removeClass('justify-content-end');  
          $el.addClass('page-content'); 
          $el.find('.posfixedcontainer').addClass('container');
          $el.find('.posfixedcol').addClass('col-lg-6 bg-soft-boxgray1 py-2');
          
        }
        if ($(this).scrollTop() < 200 && isPositionFixed){
          $el.css({'position': 'relative', 'top': '0px','transform': 'translateX(0%)', 'z-index': 'auto', 'margin-left': '0px' }); 
          $el.removeClass('page-content'); 
          //$el.removeClass('bg-soft-boxgray1');  
          $el.addClass('justify-content-end'); 
          $el.removeClass('justify-content-center');  
          $el.find('.posfixedcontainer').removeClass('container');
          $el.find('.posfixedcol').removeClass('col-lg-6 py-2 bg-soft-boxgray1 py-2');
        } 
    });
    

}

scroll('.editable-enabled-btn');