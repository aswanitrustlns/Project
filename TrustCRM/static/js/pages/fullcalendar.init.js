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

            var addEvent=$("#event-modal");
            var modalTitle = $("#modal-title");
            var formEvent = $("#form-event");
            var selectedEvent = null;
            var newEventData = null;
            var forms = document.getElementsByClassName('needs-validation');
            var selectedEvent = null;
            var newEventData = null;
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
            var defaultEvents = [
                
        ];

           // var draggableEl = document.getElementById('external-events');
            var calendarEl = document.getElementById('calendar');

            function addNewEvent(info) {
                addEvent.modal('show');
                formEvent.removeClass("was-validated");
                formEvent[0].reset();

                $("#event-title").val();
                $('#event-category').val();
                modalTitle.text('Add Reminder');
                newEventData = info;
                console.log("Event data============================="+newEventData)
            }
            

            var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: [ 'bootstrap', 'interaction', 'dayGrid', 'timeGrid'],
                editable: true,
                droppable: true,
                selectable: true,
                defaultView: 'dayGridMonth',
                themeSystem: 'bootstrap',
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
                },
                eventClick: function(info) {
                    addEvent.modal('show');
                    formEvent[0].reset();
                    selectedEvent = info.event;
                    $("#event-title").val(selectedEvent.title);
                    $('#event-category').val(selectedEvent.classNames[0]);
                    newEventData = null;
                    modalTitle.text('Edit Event');
                    newEventData = null;
                },
                dateClick: function(info) {
                    addNewEvent(info);
                },
                events : defaultEvents
            });
            // calendar.render();
            $( document ).ready(function() {

                calendar.render();

         

               

  });
            
             /*Add new event*/
            // Form to add new event

            $(formEvent).on('submit', function(ev) {
                ev.preventDefault();
                var inputs = $('#form-event:input').val();
                var updatedTitle = $("#eventtitle").val();
                var updatedCategory =  $('#event-category').val();
                var timer=$("#event-timepicker").val()
               
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
                        var newEvent = {
                            title: updatedTitle,
                            start: newEventData.date,
                            allDay: newEventData.allDay,
                            className: updatedCategory
                        }
                        calendar.addEvent(newEvent);
                        console.log("subject----"+subject)
                        console.log("ticket==="+ticket)
                        console.log("time chosen-----"+timer)
                        console.log("Detials==="+updatedTitle)
                        console.log("Category====="+updatedCategory)
                        console.log("All day-----"+newEventData.date)
                        var remDate=formatDate(newEventData.date)
                        sendReminder(ticket,timer,updatedTitle,updatedCategory,remDate)
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