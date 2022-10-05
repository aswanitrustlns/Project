/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Calendar init js
*/

!function($) {
    "use strict";

    var CalendarPage = function() {};

    CalendarPage.prototype.init = function() {

            
            var selectedEvent = null;
            
            var forms = document.getElementsByClassName('needs-validation');
            var selectedEvent = null;
           
            var eventObject = null;
            /* initialize the calendar */
            var date = new Date();
            var d = date.getDate();
            var m = date.getMonth();
            var y = date.getFullYear();
            var Draggable = FullCalendarInteraction.Draggable;
            //var externalEventContainerEl = document.getElementById('external-events');
            // init dragable
            /*new Draggable(externalEventContainerEl, {
                itemSelector: '.external-event',
                eventData: function (eventEl) {
                    return {
                        title: eventEl.innerText,
                        className: $(eventEl).data('class')
                    };
                }
            });*/
           

           // var draggableEl = document.getElementById('external-events');
            

            
            

            // calendar.render();
            $( document ).ready(function() {
                
            

         

                $('a[href="#actions-reminders-tab"]').on('click',function(){



                 $('.fc-dayGridMonth-button').trigger('click') ;

                })

               

  });
            
             /*Add new event*/
            // Form to add new event

            $(formEvent).on('submit', function(ev) {
                ev.preventDefault();
                var inputs = $('#form-event:input').val();
                var updatedTitle = $("#eventtitle").val();
                var updatedCategory =  $('#event-category').val();
                var timer=$("#event-timepicker").val()
                var remDate
                // validation
                if (forms[0].checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                        forms[0].classList.add('was-validated');
                } else {
                    if(selectedEvent){
                        selectedEvent.setProp("title", updatedTitle);
                        selectedEvent.setProp("classNames", [updatedCategory]);
                    } else {
                        ev.preventDefault()
                         console.log("Inputsssssss"+inputs)
                        var ticket=document.getElementById("ticketno").value
                        // var subject=$("#subject").val()
                        // var newEvent = {
                        //     title: updatedTitle,
                        //     start: newEventData.date,
                        //     allDay: newEventData.allDay,
                        //     className: updatedCategory
                        // }
                        // calendar.addEvent(newEvent);
                        
                        console.log("Reminder flag==================================="+reminderflag)
                        if(newEventData.date==undefined || newEventData==""){
                            remDate=formatDate(newEventData)
                        }else{
                            remDate=formatDate(newEventData.date)
                        }
                       
                        sendReminder(ticket,timer,updatedTitle,updatedCategory,remDate,reminderflag)
                    }
                    addEvent.modal('hide');
                }
            });

            $("#btn-delete-event").on('click', function(e) {
                if (selectedEvent) {
                    selectedEvent.remove();
                    selectedEvent = null;
                    addEvent.modal('hide');
                }
            });

            $("#btn-new-event").on('click', function(e) {
                addNewEvent({date: new Date(YYYY-MM-DD), allDay: true});
            });

    },
    //init
    $.CalendarPage = new CalendarPage, $.CalendarPage.Constructor = CalendarPage
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.CalendarPage.init()
}(window.jQuery);

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}