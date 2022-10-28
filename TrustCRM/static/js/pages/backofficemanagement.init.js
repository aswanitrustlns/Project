/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Form validation Js File
*/


//$valids=1;
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
                    $valids=0;
				}
				form.classList.add('was-validated');
			}, false);
		});
	}, false);
})();



/* Form editor Init Js File
*/
// ClassicEditor
//     .create( document.querySelector( '#ckeditor-classic' ),

//     {
      
//         fontFamily: {
//             options: [
//                 'default',
//                 'Arial, Helvetica, sans-serif',
//                 'Courier New, Courier, monospace',
//                 'Georgia, serif',
//                 'Lucida Sans Unicode, Lucida Grande, sans-serif',
//                 'Tahoma, Geneva, sans-serif',
//                 'Times New Roman, Times, serif',
//                 'Trebuchet MS, Helvetica, sans-serif',
//                 'Verdana, Geneva, sans-serif'
//             ],
//             supportAllValues: true
//         },
//         // https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-size-feature
//         fontSize: {
//             options: [ 10, 12, 14, 'default', 18, 20, 22 ],
//             supportAllValues: true
//         },

//         extraPlugins: 'uploadimage',
//         uploadUrl: '/apps/ckfinder/3.4.5/core/connector/php/connector.php?command=QuickUpload&type=Files&responseType=json',
//         filebrowserImageBrowseUrl: '/apps/ckfinder/3.4.5/ckfinder.html?type=Images',
//         filebrowserUploadUrl: '/apps/ckfinder/3.4.5/core/connector/php/connector.php?command=QuickUpload&type=Files',
//         filebrowserImageUploadUrl: '/apps/ckfinder/3.4.5/core/connector/php/connector.php?command=QuickUpload&type=Images',
//         } 
//      )
//     .then( function(editor) {
//         editor.model.document.on('change:data', () => {
//             someContent = editor.getData();
//             console.log(someContent);
//         })
      
//         //editor.ui.view.editable.element.style.height = '100px';

       
//     } )
//     .catch( function(error) {
//         console.error(error);
//     } 
    
//     );

let editorinstance;
ClassicEditor
    .create( document.querySelector('#editor'),

    { 
        ckfinder: {
        uploadUrl: '/media'
        
    },   
        fontFamily: {
            options: [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Lucida Sans Unicode, Lucida Grande, sans-serif',
                'Tahoma, Geneva, sans-serif',
                'Times New Roman, Times, serif',
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif'
            ],
            supportAllValues: true
        },
        // https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-size-feature
        fontSize: {
            options: [ 10, 12, 14, 'default', 18, 20, 22 ],
            supportAllValues: true
        },
        
    } 
     )
    .then( editor => {
        editorinstance =editor;
        console.log( editor );
    },function(editor) {

        
        editor.ui.view.editable.element.style.height = '100px';

       
    } )
    .catch( function(error) {
        console.error(error);
    } 
    
    );
function onloadEditmode($id,$class) {
    $('#'+$id).find('select').attr("disabled", "disabled");
    $('#'+$id).find('input').attr("disabled", "disabled");
    $('#'+$id).removeClass($class);
}

//Table select on change
function selectUpdate($this){
    //$this= $(this);
    //console.log($($this).find('option').filter(":selected").val());//Try this for value...

  

     if ($($this).find('option').filter(":selected").val()==0) {
            $this.style.backgroundColor="rgba(0, 165, 79, 0.15)";
            $this.style.color="rgba(0, 165, 79, 1)";
      }
      else if ($($this).find('option').filter(":selected").val()==1) {
        $this.style.backgroundColor ="rgba(221, 174, 6, 0.15)";
        $this.style.color="rgba(221, 174, 6, 1)";

      }
      
      else  if($($this).find('option').filter(":selected").val()==2){
        $this.style.backgroundColor ="rgba(255, 3, 3, 0.15)";
        $this.style.color="rgba(255, 3, 3, 1)";

      }

   
}

//intTel
// var intTel = function () {

//     var input = document.querySelector("#phone"),
//     input2 = document.querySelector("#phone2"),
//     errorMsg = document.querySelector("#error-msg"),
//     validMsg = document.querySelector("#valid-msg"),
//     errorMsg2 = document.querySelector("#error-msg2"),
//     validMsg2 = document.querySelector("#valid-msg2");

//     // here, the index maps to the error code returned from getValidationError - see readme
//     var errorMap = ["Invalid number","Invalid country code", "Too short", "Too long", "Invalid number"];

//     var reset = function ($input, $errorMsg, $validMsg) {
//         $input.classList.remove("error");
//         $input.classList.remove("error");
//         $errorMsg.innerHTML = "";
//         $errorMsg.classList.add("hide");
//         $validMsg.classList.add("hide");

//     };
//     var blur = function ($input, $errorMsg, $validMsg, $iti) {


//         $input.addEventListener('blur', function () {
//             reset($input, $errorMsg, $validMsg);
//             if ($input.value.trim()) {
//                 if ($iti.isValidNumber()) {
//                     $validMsg.classList.remove("hide");
//                 } else {
//                     $input.classList.add("error");
//                     var errorCode = iti.getValidationError();
//                     $errorMsg.innerHTML = errorMap[errorCode];
//                     $errorMsg.classList.remove("hide");

//                 }
//             }
//         });
//     }

//     var iti = window.intlTelInput(input, {
//         // any initialisation o,ptions go here
//         //nationalMode: true,
//         initialCountry: "auto",
//         geoIpLookup: function (callback) {
//             $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
//                 var countryCode = (resp && resp.country) ? resp.country : "us";
//                 callback(countryCode);
//             });
//         },
//         placeholderNumberType: 'MOBILE',
//         utilsScript: "assets/js/pages/utils.init.js?1638200991544"
//     });

//     // on blur: validate
//     blur(input, errorMsg, validMsg, iti);
//     // on keyup / change flag: reset
//     input.addEventListener('change', reset(input, errorMsg, validMsg));
//     input.addEventListener('keyup', reset(input, errorMsg, validMsg));


//     var iti2 = window.intlTelInput(input2, {
//         initialCountry: "auto",
//         geoIpLookup: function (callback) {
//             $.get('https://ipinfo.io', function () { }, "jsonp").always(function (resp) {
//                 var countryCode = (resp && resp.country) ? resp.country : "us";
//                 callback(countryCode);
//             });
//         },

//         placeholderNumberType: 'MOBILE',

//         utilsScript: "assets/js/pages/utils.init.js?1638200991544"
//     });


//     // on blur: validate
//     blur(input2, errorMsg2, validMsg2, iti2);
//     // on keyup / change flag: reset
//     input.addEventListener('change', reset(input2, errorMsg2, validMsg2));
//     input.addEventListener('keyup', reset(input2, errorMsg2, validMsg2));
//     // on blur: validate

// }

// intTel();

//simpleBar Init
const simpleBarJournal = new SimpleBar(document.getElementById('journal-block'));
// const simpleBarChatlog = new SimpleBar(document.getElementById('chat-block'));
const simpleBarReademail = new SimpleBar(document.getElementById('read-email-content'));
const simpleBarticketsummary=new SimpleBar(document.getElementById('ticketsummary'));
$('#ticketsummary').css('max-height', $('#formtype_account').innerHeight()-100+'px');
//$('#journal-block').css('max-height', $('#formtype_account').innerHeight()-300+'px');

//ticket block and journal block on  nav link click
$('.nav-link').on('click',function(){
    $('#ticketsummary').css('max-height', $('#formtype_account').innerHeight()-100+'px');
    $('#journal-block').css('max-height', $('#formtype_contact').innerHeight()-200+'px');
    simpleBarJournal.getScrollElement().scrollTop = simpleBarJournal.getScrollElement().scrollHeight;
});

//ticket block and journal block on window resize
window.onresize = function(event) {
    $('#ticketsummary').css('max-height', $('#formtype_account').innerHeight()-100+'px');
    $('#journal-block').css('max-height', $('#formtype_contact').innerHeight()-200+'px');
};

//Document Ready
$(document).ready(function () {
    flatpickr('#dob', {
        //inline: true,
        dateFormat: "M-d-Y",
        //defaultDate: new Date(),
    });
    flatpickr('#event-timepicker', {
        //inline: true,
		"allowInput":true,
        altInput: true,
        mode: "single",
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
    });
    


});


//changed js on from here
const myMediaQuery = window.matchMedia('(min-width: 1498px)');
function setHeight($elm,$elmIndex,$elmgetH,$elmsetH){

    //get the maxHeight using innerHeight() function
    var MaxHeight = $($elm).map(function ()  
    {

        return $(this).eq($elmIndex).find($elmgetH).innerHeight();
    }).get();
    //let myMediaQuery = window.matchMedia('(min-width: 1498px)');
    function widthChangeCallback(myMediaQuery) {
        if(myMediaQuery.matches) {
            $($elmsetH).css('height' , MaxHeight+'px' );
        } else {
            $($elmsetH).parents('.getheight ').eq(1).find(' .card-body').css('height' , MaxHeight+'px' );
           
        }
    }
    //myMediaQuery.addEventListener('change', widthChangeCallback);
    widthChangeCallback(myMediaQuery);
    
}
//setHeight('#getheight-container0 .getheight', 0, '#formtypeleads_personals', '#getheight-container0 .getheight  .card-body');
//myMediaQuery.addEventListener('change', setHeight('#getheight-container0 .getheight', 0, '#formtypeleads_personals', '#getheight-container0 .getheight  .card-body'));




//to submit form


function mysubmitformsset(){

	$is_invalid=0;
	 const formp = document.querySelectorAll('.formsset');
	 Array.prototype.slice.call(formp).forEach((form) => {
		 //alert(form.id);
		 $s=form.checkValidity();
		 //alert("Valid:"+$s);
		 if(!$s){
			 $is_invalid=1;
			 form.reportValidity();
             form.classList.add('was-validated');
		 }
	 });
	 //alert("FinalValidity:"+$is_invalid);
}



//colorswitch

var multipleswitchcolor=($this,$activecolor,$defaultcolor,$class,$activeclass)=>{
            $($this).parents('.'+$class).addClass($activeclass);
            $($this).parents('.'+$activeclass).siblings($class).removeClass($activeclass);
            $($this).css('backgroundColor',$activecolor );
            $($this).siblings().css('backgroundColor',$defaultcolor );
            $($this).parents('.'+$activeclass).siblings('.'+$class).find('.btn').css('backgroundColor',$defaultcolor );     
    
}
//tab-switch
var tabswitchemail=($this)=>{  
             let id='#'+$($this).attr('data-id');
            if(id!='#read-email'){
                $($this).css('backgroundColor','rgba(2, 126, 194, 1)');
                $($this).addClass('text-white ');
                $($this).removeClass('color-color1');
                
                $($this).siblings().css('backgroundColor',' rgba(32, 33, 52, 1)');
                $($this).siblings().addClass('color-color1');
                $($this).siblings().removeClass('text-white');
            }
            

            if($(id).hasClass('d-block')){
                $(id).removeClass('d-none');
                $(id).siblings().removeClass('d-block');
                $(id).siblings().addClass('d-none'); 
            }
            else
            {
             $(id).addClass('d-block');
             $(id).removeClass('d-none');
             $(id).siblings().removeClass('d-block');
             $(id).siblings().addClass('d-none');
            }
}
    









