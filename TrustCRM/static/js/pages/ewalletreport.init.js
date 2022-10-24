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

    
    var table = $('#datatableewreport').DataTable({
        responsive: true,
        //orderCellsTop: true,
         paging: false,
         ordering: false,
         info:false,
         fixedHeader: true,
         buttons: [ 'csv'],
     });

    table.buttons().container()
    .appendTo('#datatable-buttons_wrapper ');
    $('#datatable-buttons_wrapper .dt-buttons').find('.btn').eq(0).prepend('<img src="static/images/document-text.png" class="me-1">' + 'Export to ');
});

//