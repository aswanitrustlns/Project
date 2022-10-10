/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/
//.DataTable.datetime('D MMM YYYY');

$(document).ready(function () {
    var table = $('#datatableseminar-confirm').DataTable({
        responsive: true,
        //orderCellsTop: true,
        paging: true,
        ordering: true,
         info: true,
         fixedHeader: true,
        
     });

     $('#myinputsearch-semconf').keyup(function(){
        table.search($(this).val()).draw();
    })

    //Flat Picker Date
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
    let flatpickerfromdate=flatpickr('#fromdate-semr', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        //altInput: true,
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        //enableTime: false,
        altInput: true, // Human Readable
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        

    });
    $("#load-btn-sc"
    ).click(function() {
        flatpickerfromdate.clear();
        flatpickertodate.clear();
        // flatpickr.clear();
        
     })
     


});

//const simpleSalesreport = new SimpleBar(document.getElementById('seminarreport'));