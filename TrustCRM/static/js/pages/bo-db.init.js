/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Dashboard Init Js File
*/









function switchtab($this,$displaytab,$hiddentab) {
    $($displaytab).addClass('d-block');
 
    $($displaytab).removeClass('d-none');
    $($hiddentab).addClass('d-none');
    $($hiddentab).removeClass('d-block');  
   
    
    
}


//#spline_area


//function renderChart($id){

    //var chart = new ApexCharts(
        //document.querySelector($id),
        //options
    //);
    
    //chart.render();


//}


$(document).ready(function () {
var table1 = $('#dtpendingcryptoapproval').DataTable({
    //searching: false,
    responsive: true,
    //orderCellsTop: true,
    paging: false,
    ordering: true,
    info: false,
    //scrollY:  150,
    deferRender:    true,
    scroller:       true,
    fixedHeader: true,
    
});
var table2 = $('#dtmissingdocuments').DataTable({
    //searching: false,
    responsive: true,
    //orderCellsTop: true,
    paging: false,
    info: false,
    ordering: true,
    //scrollY: 100+'%',
    deferRender:    true,
    scroller: true,
    fixedHeader: true,
    
});
var table3 = $('#dtpendingccapproval').DataTable({
    //searching: false,
    responsive: true,
    //orderCellsTop: true,
    paging: false,
    info: false,
    ordering: true,
    //scrollY: 100+'%',
    deferRender:    true,
    scroller: true,
    fixedHeader: true,
    
});
var table4 = $('#dtpendingtransations').DataTable({
    searching: false,
    responsive: true,
    //orderCellsTop: true,
    //paging: false,
     ordering: true,
     info: false,
     lengthChange: false ,
     fixedHeader: true,
    
 });


$('table').scrollTableBody();

});











