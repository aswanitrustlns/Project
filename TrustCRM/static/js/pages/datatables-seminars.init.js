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
    info: false,
   fixedHeader: true,
   buttons: ['copy', 'excel', 'pdf'],
  


});

table.buttons().container()
.appendTo('#datatable-buttons_wrapper ');
 

$('#myinputsearch').keyup(function(){
    table.search($(this).val()).draw() ;
})

});


