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
    (minDateFilter = ""),
      (maxDateFilter = ""),
      flatpickr("#datepicker-range", {
        allowInput: !0,
        dateFormat: "dd.mm.yyyy",
        mode: "range",
        altInput: !0,
        onChange: function (e, t, a) {
          var i = $("#datatableleads").DataTable();
          "" == e && i.draw();
        },
        onReady: function (e, t, a) {},
        onClose: function (e, t, a) {
          var i = $("#datatableleads").DataTable();
          (minDateFilter = Date.parse(e[0])),
            (maxDateFilter = Date.parse(e[1])),
            $.fn.dataTable.ext.search.push(function (e, t, a) {
              t = Date.parse(t[$(this).index() + 1]);
              return !!(
                (isNaN(minDateFilter) && isNaN(maxDateFilter)) ||
                (isNaN(minDateFilter) && t <= maxDateFilter) ||
                (minDateFilter <= t && isNaN(maxDateFilter)) ||
                (minDateFilter <= t && t <= maxDateFilter)
              );
            }),
            i.draw();
        },
      });
  });