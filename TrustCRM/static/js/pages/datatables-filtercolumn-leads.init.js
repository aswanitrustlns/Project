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
   $('#datatableleads thead tr')
   .clone(true)
   .addClass('filters')
   .appendTo('#datatableleads thead');
   $("#pending").show()
   $("#resolved").hide()
   $("#dormant").hide()
   

var table = $('#datatableleads').DataTable({
   responsive: true,
   orderCellsTop: true,
   fixedHeader: true,
   initComplete: function () {
       var api = this.api();
       // For each column
       api
           .columns()
           .eq(0)
           .each(function (colIdx) {
               var column = this;
               // Set the header cell to contain the input element

               var cell = $('.filters th').eq(
                   $(api.column(colIdx).header()).index()
               );
               var title = $(cell).text();
               var id = $(cell).attr('data-id');
               //var datatext=$(cell).attr('data-text');
               var select1 = $('<select   id="' + id + '" placeholder="' + title + '"  class="fs-14 form-control w-100"><option value=""></option></select>');
               if ($(cell).attr('data-text') == 'select') {
                   //console.log($(cell).index());
                   api.column($(cell).index())
                       .data()
                       .unique()
                       .sort()
                       .each(function (d, j) {


                           select1.append('<option value="' + d + '">' + d + '</option>');

                       });
                   $(cell).html(select1);




               } else {
                   $(cell).html('<input type="text" id="' + id + '" placeholder="' + title + '"  class="fs-14"   />');
               }


               // On every keypress in this input
               $(
                   'input',
                   $('.filters th').eq($(api.column(colIdx).header()).index())
               )
                   .off('keyup change')
                   .on('change', function (e) {

                       if ($(this).attr('id') == 'datepicker-range') {
                           console.log("Heloooo");

                           //var vals=this.value ;



                       } else {
                           //console.log($(this).attr('id'));


                           // Get the search value
                           $(this).attr('title', $(this).val());

                           //var vals=this.value ;

                           var regexr = '({search})'; //$(this).parents('th').find('select').val();

                           var cursorPosition = this.selectionStart;
                           // Search the column for that value
                           api
                               .column(colIdx)
                               .search(
                                   this.value != ''
                                       ? regexr.replace('{search}', '(((' + this.value + ')))')
                                       : '',
                                   this.value != '',
                                   this.value == ''
                               )
                               .draw();

                       }


                   })
                   .on('keyup', function (e) {
                       e.stopPropagation();

                       $(this).trigger('change');
                       $(this)
                           .focus()[0]
                           .setSelectionRange(cursorPosition, cursorPosition);
                   });

               $(
                   'select',
                   $('.filters th').eq($(api.column(colIdx).header()).index())
               )
                   .off('keyup change')
                   .on('change', function (e) {

                       if ($(this).attr('id') == 'datepicker-range') {
                           console.log("Heloooo");

                           //var vals=this.value ;



                       } else {
                           //console.log($(this).attr('id'));


                           // Get the search value
                           $(this).attr('title', $(this).val());

                           //var vals=this.value ;

                           var regexr = '({search})'; //$(this).parents('th').find('select').val();

                           var cursorPosition = this.selectionStart;
                           // Search the column for that value
                           api
                               .column(colIdx)
                               .search(
                                   this.value != ''
                                       ? regexr.replace('{search}', '(((' + this.value + ')))')
                                       : '',
                                   this.value != '',
                                   this.value == ''
                               )
                               .draw();

                       }

                   })
                   .on('keyup', function (e) {
                       e.stopPropagation();

                       $(this).trigger('change');
                       $(this)
                           .focus()[0]
                           .setSelectionRange(cursorPosition, cursorPosition);
                   });
           });

   },


});



    
//dataTables('#datatableleads');
    
 // Date range vars
 minDateFilter = "";
 maxDateFilter = "";


    //Flat Picker Date
    flatpickr('#datepicker-range', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        //altInput: true,
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat: "Y-m-d",
        mode: "range",
        //enableTime: false,
        altInput: true, // Human Readable
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        onChange:
            function (selectedDates, dateStr, instance) {
              
                var table = $('#datatableleads').DataTable();
                function rangefilter(ev, picker) {
                            minDateFilter = Date.parse(selectedDates[0]);
                            maxDateFilter = Date.parse(selectedDates[1]);
                            //console.log( 'maxDateFilter'+ maxDateFilter);
                            //console.log( 'minDateFilter'+ minDateFilter);
                           // console.log( $(this).index()+1);
                            $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
                            var date = Date.parse(data[ $(this).index()+1]);
                        
                            if (
                            (isNaN(minDateFilter) && isNaN(maxDateFilter)) ||
                            (isNaN(minDateFilter) && date <= maxDateFilter) ||
                            (minDateFilter <= date && isNaN(maxDateFilter)) ||
                            (minDateFilter <= date && date <= maxDateFilter)
                            ) {
                            return true;
                            }
                            return false;
                        });
                        table.draw();
                        }

                rangefilter();
        },
        onReady: function (selectedDates, dateStr, instance) {
           
        },
          // https://codepen.io/bintux/pen/rgYeyp
        onClose: function (selectedDates, dateStr, instance) {
            var table = $('#datatableleads').DataTable();
            function rangefilter(ev, picker) {
                            minDateFilter = Date.parse(selectedDates[0]);
                            maxDateFilter = Date.parse(selectedDates[1]);
                            //console.log( 'maxDateFilter'+ maxDateFilter);
                            //console.log( 'minDateFilter'+ minDateFilter);
                           // console.log( $(this).index()+1);
                            $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
                            var date = Date.parse(data[ $(this).index()+1]);
                        
                            if (
                            (isNaN(minDateFilter) && isNaN(maxDateFilter)) ||
                            (isNaN(minDateFilter) && date <= maxDateFilter) ||
                            (minDateFilter <= date && isNaN(maxDateFilter)) ||
                            (minDateFilter <= date && date <= maxDateFilter)
                            ) {
                            return true;
                            }
                            return false;
                        });
                        table.draw();
                        }

            rangefilter();

                         //console.log(selectedDates.attr('value'));
          
            
        }

    });


    //Flat Picker Date
    let flatpickertodate=flatpickr('#todate', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        //altInput: true,
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat: "Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        

    });

    //Flat Picker Date
    let flatpickerfromdate=flatpickr('#fromdate', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        //altInput: true,
        "allowInput": true,
        dateFormat: "Y-m-d",//MMMM Do YYYY
        altFormat: "Y-m-d",
        mode: "single",
        enableTime: false,
        altInput: true, // Human Readable
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        //locale: { firstDayOfWeek: 1},

        

    });
   

});
var addColor=function ($this,$class,$textcolor){
    
    console.log("This is======"+$this);
    selId=$($this).attr('id')
    if(selId=="pending-switch"){
        $("#pending").show()
        $("#resolved").hide()
        $("#dormant").hide()
    }
    if(selId=="resolved-switch"){
        $("#pending").hide()
        $("#resolved").show()
        $("#dormant").hide()
    }
    if(selId=="dormant-switch"){
        $("#pending").hide()
        $("#resolved").hide()
        $("#dormant").show()
    }
    $("#selected_tab").val(selId)
    console.log("Selected tab Id===="+selId)
    if($($this).hasClass($class)){
        $($this).removeClass($class);
        $($this).addClass($textcolor);
    }
    else{
        $($this).addClass($class);
        $($this).removeClass($textcolor);
        $($this).siblings().removeClass($class);
        $($this).siblings().addClass($textcolor);
    }

}


