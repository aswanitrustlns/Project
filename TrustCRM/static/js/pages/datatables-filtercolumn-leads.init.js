$(document).ready(function () {
    $("#datatableleads thead tr")
      .clone(!0)
      .addClass("filters")
      .appendTo("#datatableleads thead");
    $("#datatableleads").DataTable({
      responsive: !0,
      orderCellsTop: !0,
      fixedHeader: !0,
      initComplete: function () {
        var o = this.api();
        o.columns()
          .eq(0)
          .each(function (t) {
            var e = $(".filters th").eq($(o.column(t).header()).index()),
              a = $(e).text(),
              i = $(e).attr("data-id"),
              n = $(
                '<select   id="' +
                  i +
                  '" placeholder="' +
                  a +
                  '"  class="fs-14 form-control w-100"><option value=""></option></select>'
              );
            "select" == $(e).attr("data-text")
              ? (o
                  .column($(e).index())
                  .data()
                  .unique()
                  .sort()
                  .each(function (e, t) {
                    n.append('<option value="' + e + '">' + e + "</option>");
                  }),
                $(e).html(n))
              : $(e).html(
                  '<input type="text" id="' +
                    i +
                    '" placeholder="' +
                    a +
                    '"  class="fs-14"   />'
                ),
              $("input", $(".filters th").eq($(o.column(t).header()).index()))
                .off("keyup change")
                .on("change", function (e) {
                  "datepicker-range" == $(this).attr("id")
                    ? console.log("Heloooo")
                    : ($(this).attr("title", $(this).val()),
                      this.selectionStart,
                      o
                        .column(t)
                        .search(
                          "" != this.value
                            ? "({search})".replace(
                                "{search}",
                                "(((" + this.value + ")))"
                              )
                            : "",
                          "" != this.value,
                          "" == this.value
                        )
                        .draw());
                })
                .on("keyup", function (e) {
                  e.stopPropagation(),
                    $(this).trigger("change"),
                    $(this)
                      .focus()[0]
                      .setSelectionRange(cursorPosition, cursorPosition);
                }),
              $("select", $(".filters th").eq($(o.column(t).header()).index()))
                .off("keyup change")
                .on("change", function (e) {
                  "datepicker-range" == $(this).attr("id")
                    ? console.log("Heloooo")
                    : ($(this).attr("title", $(this).val()),
                      this.selectionStart,
                      o
                        .column(t)
                        .search(
                          "" != this.value
                            ? "({search})".replace(
                                "{search}",
                                "(((" + this.value + ")))"
                              )
                            : "",
                          "" != this.value,
                          "" == this.value
                        )
                        .draw());
                })
                .on("keyup", function (e) {
                  e.stopPropagation(),
                    $(this).trigger("change"),
                    $(this)
                      .focus()[0]
                      .setSelectionRange(cursorPosition, cursorPosition);
                });
          });
      },
    });


    minDateFilter = "";
    maxDateFilter = "";


    flatpickr('#datepicker-range', {

       
      "allowInput": true,
      dateFormat: "dd.mm.yyyy",//MMMM Do YYYY
      mode: "range",
     
      altInput: true,       

      onChange:
          function (selectedDates, dateStr, instance) {

              var table = $('#datatableleads').DataTable();
              if(selectedDates==''){

                  table.draw();
              }
             

              //console.log("Helooo");
          },
      onReady: function (selectedDates, dateStr, instance) {
          

      },
        
      onClose: function (selectedDates, dateStr, instance) {
          var table = $('#datatableleads').DataTable();
          function rangefilter(ev, picker) {
                          minDateFilter = Date.parse(selectedDates[0]);
                          maxDateFilter = Date.parse(selectedDates[1]);
                          
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
      }

  });


  flatpickr('#todate', {

  
      "allowInput": true,
      dateFormat: "Y-m-d",//MMMM Do YYYY
      mode: "single",
     
      altInput: true, // Human Readable
     

      

  });

  
  flatpickr('#fromdate', {

      "allowInput": true,
      dateFormat: "Y-m-d",//MMMM Do YYYY
      mode: "single",
     
      altInput: true, // Human Readable
  
      

  });

  });