/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/
//.DataTable.datetime('D MMM YYYY');

$(document).ready(function () {
    //const simpleUserActivity = new SimpleBar(document.getElementById('useractivity'));
    //const  simpleUploadDocumentsDetails  = new SimpleBar(document.getElementById('uploaddocumentsdetails'));
     //table1
    var table1 = $('#datatableiblive').DataTable({
         responsive: true,
         paging: true,
         lengthChange: false ,
         ordering: true,
         info:true,
         fixedHeader: true,
         buttons: [ 'print','copy','csv'],
     });
    //table1 btns
    table1.buttons().container()
    .appendTo('#datatable-buttons_wrapper1 ');
    $('#datatable-buttons_wrapper1 .dt-buttons').find('.btn').eq(0).prepend('<img src="assets/images/printer.png" class="me-1">');
    $('#datatable-buttons_wrapper1 .dt-buttons').find('.btn').eq(1).prepend('<img src="assets/images/copy.png" class="me-1">');
    $('#datatable-buttons_wrapper1 .dt-buttons').find('.btn').eq(2).prepend('<img src="assets/images/document-text.png" class="me-1">');
    $('#datatable-buttons_wrapper1').find('.btn').addClass('me-2 d-inline-block flex-shrink-0  my-1 bg-soft-gunmetal border-0');
    $('#datatable-buttons_wrapper1').find('.btn-group').addClass('flex-xl-nowrap');
    $('#datatable-buttons_wrapper1').find('.btn-group').removeClass('flex-wrap');
    $('#myinputsearch1').keyup(function(){
        table1.search($(this).val()).draw() ;
    })

    //table2 
    var table2 = $('#datatableibpending').DataTable({
        responsive: true,
        paging: true,
        lengthChange: false ,
        ordering: true,
        info:true,
        fixedHeader: true,
        buttons: [ 'print','copy','csv'],
    });
   //table2 btns
   table2.buttons().container()
   .appendTo('#datatable-buttons_wrapper2 ');
   $('#datatable-buttons_wrapper2 .dt-buttons').find('.btn').eq(0).prepend('<img src="assets/images/printer.png" class="me-1">');
   $('#datatable-buttons_wrapper2 .dt-buttons').find('.btn').eq(1).prepend('<img src="assets/images/copy.png" class="me-1">');
   $('#datatable-buttons_wrapper2 .dt-buttons').find('.btn').eq(2).prepend('<img src="assets/images/document-text.png" class="me-1">');
   $('#datatable-buttons_wrapper2').find('.btn').addClass('me-2 d-inline-block flex-shrink-0  my-1 bg-soft-gunmetal border-0');
   $('#datatable-buttons_wrapper2').find('.btn-group').addClass('flex-xl-nowrap');
   $('#datatable-buttons_wrapper2').find('.btn-group').removeClass('flex-wrap');
   $('#myinputsearch2').keyup(function(){
       table2.search($(this).val()).draw() ;
   })



   //table2 
   var table3 = $('#datatableibrejected').DataTable({
    responsive: true,
    paging: true,
    lengthChange: false ,
    ordering: true,
    info:true,
    fixedHeader: true,
    buttons: [ 'print','copy','csv'],
    });
    //table3 btns
    table3.buttons().container()
    .appendTo('#datatable-buttons_wrapper3');
    $('#datatable-buttons_wrapper3 .dt-buttons').find('.btn').eq(0).prepend('<img src="assets/images/printer.png" class="me-1">');
    $('#datatable-buttons_wrapper3 .dt-buttons').find('.btn').eq(1).prepend('<img src="assets/images/copy.png" class="me-1">');
    $('#datatable-buttons_wrapper3 .dt-buttons').find('.btn').eq(2).prepend('<img src="assets/images/document-text.png" class="me-1">');
    $('#datatable-buttons_wrapper3').find('.btn').addClass('me-2 d-inline-block flex-shrink-0  my-1 bg-soft-gunmetal border-0');
    $('#datatable-buttons_wrapper3').find('.btn-group').addClass('flex-xl-nowrap');
    $('#datatable-buttons_wrapper3').find('.btn-group').removeClass('flex-wrap');
    $('#myinputsearch3').keyup(function(){
    table3.search($(this).val()).draw() ;
    })
    //flat picker Date1

    let flatpickerFromdate1=flatpickr('#Fromdate1', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
    });

   
    let flatpickertodate1=flatpickr('#Todate1', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable
    });
    //flat picker Date2
    let flatpickerFromdate2=flatpickr('#Fromdate2', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
    });

  
    let flatpickertodate2=flatpickr('#Todate2', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable
    });
    //flat picker Date3
    let flatpickerFromdate3=flatpickr('#Fromdate3', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
    });

    let flatpickertodate3=flatpickr('#Todate3', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable
    });

    //
    $('.nav-item').on('click',function(){
        //console.log($(this));
        $(this).find('a').addClass('bg-soft-purple  text-white');
        $(this).find('a').removeClass('color-color1');
        $(this).siblings().find('a').removeClass('bg-soft-purple text-white');
        $(this).siblings().find('a').addClass(' color-color1 bg-soft-secondarycolor');
    })
});

