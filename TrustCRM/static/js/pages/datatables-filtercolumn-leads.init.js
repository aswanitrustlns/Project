/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/


$(document).ready(function () {

    var minDate,maxDate;

    
    // Setup - add a text input to each footer cell
    $('#datatableleads thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#datatableleads thead');
 
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
                   
                    // Set the header cell to contain the input element
                  
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    var id = $(cell).attr('data-id');
                    
                    $(cell).html('<input type="text" id="'+id+'" placeholder="' + title + '"  class="fs-14"   />');
                    
                    // On every keypress in this input
                    $(
                        'input',
                        $('.filters th').eq($(api.column(colIdx).header()).index())
                    )
                        .off('keyup change')
                        .on('change', function (e) {

                            console.log($(this).attr('id'));

                            if($(this).attr('id')=='datepicker-range'){
                                
                                api
                                .column(colIdx)
                                .search(
                                        function( data, colIdx ) {
                                            //var min = minDate;
                                            // var max = maxDate;
                                            // console.log(min);
                                                //date = new Date( colIdx[0] );
                                            var min = minDate;
                                            var max = maxDate;
                                            var date = new Date(data[0]);
                                            

                                            //colIdx
                                     
                                            if (
                                                ( min === null && max === null ) ||
                                                ( min === null && date <= max ) ||
                                                ( min <= date   && max === null ) ||
                                                ( min <= date   && date <= max )
                                            ) {
                                                return true;
                                                console.log('searching-date-start' +min  );
                                                console.log('searching-date-endt' +max  );
                                            }
                                            return false;
                                            console.log('searching-date-start' +min  );
                                            console.log('searching-date-endt' +max  );
                                        }
                                    
                                ).draw();
                               

                                
                            }
                            else{

                                    // Get the search value
                                $(this).attr('title', $(this).val());
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
    

    //Flat Picker Date

    flatpickr('#datepicker-range', {

        //const fp = flatpickr(".test-calendar", {  altFormat: "F j, Y", dateFormat: "Y-m-d", showMonths: 3, disableMobile: true, inline: true, mode: "range", 
        //altInput: true,
        "allowInput":true,
        dateFormat:"Y-m-d",
        mode: "range",
        altInput: true, // Human Readable
        //minDate: new Date().fp_incr(-60), // 60 days from today
        //maxDate: defaultEnd,
        locale: { firstDayOfWeek: 1},

        onChange:
         function (selectedDates, dateStr, instance) { 
            
            console.log('dateStronChange'+dateStr); 
        
        }, 
        onReady: function(selectedDates, dateStr, instance){ 
            console.log('dateStronReady'+dateStr);
         } ,

        onClose: function(selectedDates, dateStr, instance) {
              minDate =  selectedDates[0].toISOString().slice(0, 10);
              maxDate  = selectedDates[1].toISOString().slice(0, 10);
              //this.$emit('change', {  minDate, maxDate });  
            console.log('minDate'+minDate);
            console.log('maxDate'+maxDate);

             // Custom filtering function which will search data in column four between two values
           
        }
    });

  
 
   
    

    

    
});
