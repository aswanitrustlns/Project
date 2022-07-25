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
	// window.addEventListener('load', function () {
	// 	// Fetch all the forms we want to apply custom Bootstrap validation styles to
	// 	var forms = document.getElementsByClassName('needs-validation');
	// 	// Loop over them and prevent submission
	// 	var validation = Array.prototype.filter.call(forms, function (form) {
	// 		form.addEventListener('submit', function (event) {
	// 			if (form.checkValidity() === false) {
	// 				event.preventDefault();
	// 				event.stopPropagation();
	// 			}
	// 			form.classList.add('was-validated');
	// 		}, false);
	// 	});
	// }, false);
})();


// pristinejs validation

window.onload = function () {
	// pristinejs validation
	//var form = document.getElementById("pristine-valid-example");
	// var pristine = new Pristine(form);
	// form.addEventListener('submit', function (e) {
	// 	e.preventDefault();
	// 	var valid = pristine.validate();
	// 	//alert('Form is valid: ' + valid);

	// });

	var lead_registration=document.getElementById("lead_register")
	lead_registration.addEventListener('click',lead_validation)

	function lead_validation(e){
		e.preventDefault()
		console.log("lead validation")
		age=parseInt(document.getElementById("age").value)
		console.log(age)
		email1=document.getElementById("email1")
		email2=document.getElementById("email2")
		console.log(email1)
		console.log(email2)
		if(email1==" "&& email2==""){
			$('#email_check').prop('checked', true);
		}

		var phoneno = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
		if(mobile.value.match(phoneno)) {
		  return true;
		}
		else {
		 console.log("error")
		  return false;
		}
		console.log(typeof(age))
		if(age>18){
			
			return true
			
		}
		else{
			return false
		}
	}


	// pristinejs common validation
	// var commonform = document.getElementById("pristine-valid-common");
	// var commonformpristine = new Pristine(commonform);
	// commonform.addEventListener('submit', function (e) {
	// 	e.preventDefault();
	// 	var commonformvalid = commonformpristine.validate();
	// 	//alert('Form is valid: ' + commonformvalid);
	// });

	// validator to a specific field
	var specificfieldform = document.getElementById("pristine-valid-specificfield");
	var specificfieldpristine = new Pristine(specificfieldform);
	var specificfieldelem = document.getElementById("specificfield")

	specificfieldpristine.addValidator(specificfieldelem, function (value, el) {
		if (value.length && value[0] === value[0].toUpperCase()) {
			return true;
		}
		return false;
	}, "The first character must be capitalized", 2, false);

	specificfieldform.addEventListener('submit', function (e) {
		e.preventDefault();
		var specificfieldvalid = specificfieldpristine.validate();
		//alert('Form is valid: ' + specificfieldvalid);

	});
};

