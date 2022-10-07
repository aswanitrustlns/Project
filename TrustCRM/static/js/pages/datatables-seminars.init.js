/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/
//.DataTable.datetime('D MMM YYYY');

$(document).ready(function () {


    //var minDate,maxDate;


   // Setup - add a text input to each footer cell
   //$('#datatableleads thead tr')
   //.clone(true)
   //.addClass('filters')
   //.appendTo('#datatableleads thead');

var table = $('#datatableseminar').DataTable({
   responsive: true,
   //orderCellsTop: true,
   //paging: false,
   ordering: true,
    info: true,
    fixedHeader: true,
   buttons: [ 'print','copy','csv',],
});
flatpickr('#dob', {

       
    "allowInput":true,
    dateFormat: "Y-m-d",
    altFormat:"Y-m-d",
    
    altInput: true, // Human Readable
    

   
});
flatpickr('#Date', {

       
    "allowInput":true,
    dateFormat: "Y-m-d",
    altFormat:"Y-m-d",
   
    altInput: true, // Human Readable
    

   
});
flatpickr('#ardate', {

       
    "allowInput":true,
    dateFormat: "Y-m-d",
    altFormat:"Y-m-d",
   
    altInput: true, // Human Readable
    

   
});
flatpickr('#time', {
    //inline: true,
    "allowInput":true,
    altInput: true,
    mode: "single",
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
});
flatpickr('#artime', {
    //inline: true,
    "allowInput":true,
    altInput: true,
    mode: "single",
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
});

table.buttons().container()
.appendTo('#datatable-buttons_wrapper ');

$('#datatable-buttons_wrapper .dt-buttons').find('.btn').eq(0).prepend('<img src="static/images/printer.png" class="me-1">');
$('#datatable-buttons_wrapper .dt-buttons').find('.btn').eq(1).prepend('<img src="static/images/copy.png" class="me-1">');
$('#datatable-buttons_wrapper .dt-buttons').find('.btn').eq(2).prepend('<img src="static/images/document-text.png" class="me-1">');
$('#datatable-buttons_wrapper').find('.btn').addClass('me-2 d-inline-block flex-grow-0  my-1');

$('#myinputsearch').keyup(function(){
    table.search($(this).val()).draw() ;
})

});


