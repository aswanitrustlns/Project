/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/
//.DataTable.datetime('D MMM YYYY');

$(document).ready(function () {
   
    var table = $('#datatablebankdetails').DataTable({
        responsive: true,
        //orderCellsTop: true,
        //paging: false,
        ordering: false,
         info: true,
         fixedHeader: true,
        
     });
     $('#myinputsearch-bankdetails').keyup(function(){
        table.search($(this).val()).draw();
    })
    var table1 = $('#datatableewtransactionshistory').DataTable({
        responsive: true,
        //orderCellsTop: true,
        //paging: false,
        ordering: false,
         info: true,
         fixedHeader: true,
        
     });
     $('#myinputsearch-ewtransactionshistory').keyup(function(){
        table1.search($(this).val()).draw();
    })

    var table2 = $('#datatablemt4transactionshistory').DataTable({
        responsive: true,
        //orderCellsTop: true,
        //paging: false,
        ordering: false,
         info: true,
         fixedHeader: true,
        
     });
     $('#myinputsearch-mt4transactionshistory').keyup(function(){
        table2.search($(this).val()).draw();
    })

    var table2 = $('#datatabletransactiondetails').DataTable({
        responsive: true,
        //orderCellsTop: true,
        //paging: false,
         ordering: false,
         info: true,
         fixedHeader: true,
        
     });
     $('#myinputsearch-transactiondetails').keyup(function(){
        table2.search($(this).val()).draw();
    })
    



    ///
    let flatpickerexp=flatpickr('#expdate', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
       
        enableTime: false,
        altInput: true, // Human Readable
       
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        

    });
    let flatpickertodate=flatpickr('#todate-semr', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
       
        enableTime: false,
        altInput: true, // Human Readable
       
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        

    });

    //Flat Picker Date
    let flatpickerFromdate=flatpickr('#Fromdate', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });
     //Flat Picker Date
     let flatpickerTodate=flatpickr('#Todate', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });
     //Flat Picker Date
     let flatpickerFromdate1=flatpickr('#Fromdate1', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });
     //Flat Picker Date
     let flatpickerTodate1=flatpickr('#Todate1', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });
    let flatpickerFromdate2=flatpickr('#Fromdate2', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });
     //Flat Picker Date
     let flatpickerTodate2=flatpickr('#Todate2', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable

    });


    let tab = document.getElementsByClassName('nav-item');
    //nput.type = 'file';
    //tab.onclick = e => { 
    //var file = e.target.files[0]; 
    //$('#choosetext').text( file.name);
    //alert("hi")
    //}
    $(tab).on('click',function(e){
   //alert($(this).attr('data-title'))
      //$(this).attr('data-title');
      $('#titlemain').text(  $(this).attr('data-title'));
    })
    

});

//const simpleSalesreport = new SimpleBar(document.getElementById('seminarreport'));