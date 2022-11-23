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
    var table1 = $('#datatable').DataTable({
         responsive: true,
         paging: true,
         lengthChange: false ,
         ordering: true,
         info:true,
         fixedHeader: true,
         buttons: [ 'print','copy','csv'],
     });
 
    //table1 btns
   
   



   
    

    let flatpickerFromdate1=flatpickr('#Fromdate', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
    });

   
    let flatpickertodate1=flatpickr('#Todate', {
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat:"Y-m-d",
        mode: "single",
        altInput: true, // Human Readable
    });
   
});

