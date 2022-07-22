/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/

$(document).ready(function() {

    $('#datatableleads tbody tr:first-child th').each(function () {
        var title = $(this).text();
        //var type= $(this).attr("data-type");
        //console.log(type);
        $(this).html('<input type="text" placeholder="Search ' + title + '" />');
    });
    // DataTable
    $('#datatableleads').DataTable({
        initComplete: function () {
            // Apply the search
            this.api()
                .columns()
                .every(function () {
                    var that = this;
 
                    $('input').on('keyup change clear', function () {
                        if (that.search() !== this.value) {
                            that.search(this.value).draw();
                        }
                    });
                });
        },
    });
    //$('#datatableleads').DataTable();

    //Buttons examples
    //var table = $('#datatable-buttons').DataTable({
        //lengthChange: false,
        //buttons: ['copy', 'excel', 'pdf', 'colvis']
    //});

    //table.buttons().container()
       // .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

    //$(".dataTables_length select").addClass('form-select form-select-sm');
});