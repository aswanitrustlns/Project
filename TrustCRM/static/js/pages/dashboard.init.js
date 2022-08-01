/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Dashboard Init Js File
*/

// get colors array from the string
var pievalue;

function getChartColorsArray(chartId) {
    var colors = $(chartId).attr('data-colors');
    var colors = JSON.parse(colors);
    return colors.map(function(value){
        var newValue = value.replace(' ', '');
        if(newValue.indexOf('--') != -1) {
            var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
            if(color) return color;
        } else {
            return newValue;
        }
    })
}
function switchtab($displaytab,$hiddentab) {
    $($displaytab).addClass('d-block');
    $($displaytab).removeClass('d-none');
    $($hiddentab).addClass('d-none');
    $($hiddentab).removeClass('d-block');  
}


var seminar_data_d = seminar_daily_pie.map((item) => item.value);
var seminar_username_d = seminar_daily_pie.map((item) => item.name);
seminar_username_d=Object.values(seminar_username_d)

var seminar_data_w = seminar_weekly_pie.map((item) => item.value);
var seminar_username_w = seminar_weekly_pie.map((item) => item.name);
seminar_username_w=Object.values(seminar_username_w)


function renderSeminarPie($series,$id,$label){

    var piechartColors = getChartColorsArray($id);
    var options = {
   
    chart: {
        width: 227,
        height: 227,
        type: 'pie',
    },
    series:$series,
    labels: $label,
    colors: piechartColors,
    stroke: {
        width: 0,
    },
    legend: {
        show: false
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
        }
    }]
};

var chart = new ApexCharts(document.querySelector($id), options);
chart.render();
}
renderSeminarPie(seminar_data_d,'#weekly-seminar_d',seminar_username_d);
renderSeminarPie(seminar_data_w,'#weekly-seminar_w',seminar_username_w);

// weekly-seminar
// var piechartColors = getChartColorsArray("#weekly-seminar");

// var data = pie_data.map((item) => item.value);

// var username = pie_data.map((item) => item.name);
// username=Object.values(username)
// var options = {
//     series: data,
//     chart: {
//         width: 227,
//         height: 227,
//         type: 'pie',
//     },
//     labels: username,
//     colors: piechartColors,
//     stroke: {
//         width: 0,
//     },
//     legend: {
//         show: false
//     },
//     responsive: [{
//         breakpoint: 480,
//         options: {
//             chart: {
//                 width: 200
//             },
//         }
//     }]
// };

// var chart = new ApexCharts(document.querySelector("#weekly-seminar"), options);
// chart.render();
// 

// Leads
var piechartColors = getChartColorsArray("#leads");
var options = {
    dataLabels: {
        textAnchor: 'middle',
        position: 'center',
        distributed: false,
        style: {
            fontSize: '10px',
            //fontFamily: 'Helvetica, Arial, sans-serif',
            fontWeight: 'bold',
            colors: undefined
        },
    },
    series: leads_pie,
    chart: {
        //width: 171,
        height: 200,
        type: 'pie',
    },
    labels: ['Spoken', 'Busy', 'NoReply','WrongCalls','Resolved'],
    colors: piechartColors,
    stroke: {
        width: 0,
    },
    legend: {
        show: false
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#leads"), options);
chart.render();

// column chart1  live_accounts
function renderChart($series,$id,$catogories){

    // column chart1  live_accounts
var columnColors = getChartColorsArray($id);
var options = {
    chart: {
        height: 300,
        type: 'bar',
        toolbar: {
            show: false,
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: $series,
    colors: columnColors,
    xaxis: {
        categories: $catogories,
    },
    yaxis: {
        title: {
            text: ' ',
            style: {
                fontWeight:  '500',
              },
        }
    },
    grid: {
        borderColor: '#f1f1f1',
    },
    fill: {
        opacity: 1

    },
    tooltip: {
        y: {
            formatter: function (val) {
                return  + val + " "
            }
        }
    }
}

var chart = new ApexCharts(
    document.querySelector($id),
    options
);

chart.render(); 
    
}
var data_value_w = weekly_live.map((item) => item.value);

var username_w =weekly_live.map((item) => item.name);
username_w=Object.values(username_w)
renderChart([{data:data_value_w}], '#column_chart_live_accounts_w',username_w);



var data_value_d = daily_live.map((item) => item.value);

var username_d =daily_live.map((item) => item.name);
username_d=Object.values(username_d)
renderChart([{data:data_value_d}], '#column_chart_live_accounts_d',username_d);




// var columnColors = getChartColorsArray("#column_chart_live_accounts");
// var data_value = weekly_live.map((item) => item.value);

// var username =weekly_live.map((item) => item.name);
// username=Object.values(username)
// var options = {
//     chart: {
//         height: 300,
//         type: 'bar',
//         toolbar: {
//             show: false,
//         }
//     },
//     plotOptions: {
//         bar: {
//             horizontal: false,
//             columnWidth: '55%',
//         },
//     },
//     dataLabels: {
//         enabled: false
//     },
//     stroke: {
//         show: true,
//         width: 2,
//         colors: ['transparent']
//     },
//     series: [{
        
//         data: data_value
//     }],
//     colors: columnColors,
//     xaxis: {
//         categories: username,
//     },
//     yaxis: {
//         title: {
//             text: ' ',
//             style: {
//                 fontWeight:  '500',
//               },
//         }
//     },
//     grid: {
//         borderColor: '#f1f1f1',
//     },
//     fill: {
//         opacity: 1

//     },
//     tooltip: {
//         y: {
//             formatter: function (val) {
//                 return  + val + " "
//             }
//         }
//     }
// }

// var chart = new ApexCharts(
//     document.querySelector("#column_chart_live_accounts"),
//     options
// );

// chart.render();

// column chart2 liveaccount_statics
var columnColors = getChartColorsArray("#column_chart_leadsbysource");
var src_count = leads_status.map((item) => item.src_count);
var ticket_count = leads_status.map((item) => item.ticket_count);
var username =leads_status.map((item) => item.name);
var options = {
    chart: {
        height: 300,
        type: 'bar',
        toolbar: {
            show: false,
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name:"Source Count",
        data: src_count
    },
    {
        name:"Ticket Count",
        data: ticket_count
    },
    
],
    colors: columnColors,
    xaxis: {
    categories: username,
    },
    yaxis: {
        title: {
            text: ' ',
            style: {
                //fontWeight:  '500',
                fontFamily: 'gilorymedium'
              },
        }
    },
    grid: {
        borderColor: '#f1f1f1',
    },
    fill: {
        opacity: 1

    },
    tooltip: {
        y: {
            formatter: function (val) {
                return  + val + " "
            }
        }
    }
}
var chart = new ApexCharts(
    document.querySelector("#column_chart_leadsbysource"),
    options
);
chart.render();

// Donut chart
var donutColors = getChartColorsArray("#donut_chart_ticketdialed");
var options = {
    dataLabels: {
        enabled:false,
    },
    plotOptions: {
        pie: {
          expandOnClick: false
        }
    },
  chart: {
     
      height: 186,
      //width: 186,
      type: 'donut',
      verticalAlign: 'center',
  }, 
  series: [],
  labels: [],
  colors: donutColors,
  legend: {
      show: true,
      position: 'right',
      horizontalAlign: 'center',
      verticalAlign: 'center',
      floating: false,
      fontSize: '14px',
      fontFamily: 'Helvetica, Arial',
      offsetX: 0,

      itemMargin: {
        
        vertical: 4,
    },
  },
  responsive: [{
      breakpoint: 600,
      options: {
          chart: {
              height: 240
          },
          legend: {
              
              position: 'bottom'
          },
      }
  }]

}
var chart = new ApexCharts(
    document.querySelector("#donut_chart_ticketdialed"),
    options
  );
  chart.render()

// Donut chart

var data_d = meeting_daily_pie.map((item) => item.value);
data_d=Object.values(data_d)
var username_d = meeting_daily_pie.map((item) => item.name);
username_d=Object.values(username_d)
var data_w = meeting_weekly_pie.map((item) => item.value);
data_w=Object.values(data_w)
var username_w = meeting_weekly_pie.map((item) => item.name);
username_w=Object.values(username_w)

function renderMeetingDonut($series,$id,$label){

var donutColors = getChartColorsArray($id);

var options = {
    dataLabels: {
        enabled:false,
    },
    plotOptions: {
        pie: {
          expandOnClick: false
        }
    },
  chart: {
     
      height: 220,
      //width: 186,
      type: 'donut',
      verticalAlign: 'center',
  }, 
  series: $series,
  labels: $label,
  colors: donutColors,
  legend: {
      show: true,
      position: 'bottom',
      horizontalAlign: 'center',
      verticalAlign: 'center',
      floating: false,
      fontSize: '14px',
      fontFamily: 'gilroymedium',
      offsetX: 0,

      itemMargin: {
        
        vertical: 4,
    },
  },
  responsive: [{
      breakpoint: 600,
      options: {
          chart: {
              height: 240
          },
          legend: {
              
              position: 'bottom'
          },
      }
  }]

}
var chart = new ApexCharts(
  document.querySelector($id),
  options
);
chart.render()

}
renderMeetingDonut(data_d,"#meetings_report_d",username_d)
renderMeetingDonut(data_w,"#meetings_report_w",username_w)

//   spline_area

var month = halfyearly_bar.map((item) => item.month);
// month=Object.values(month)
var live_account = halfyearly_bar.map((item) => item.live_account);
live_account=Object.values(live_account)
var pending_account = halfyearly_bar.map((item) => item.pending_account);
pending_account=Object.values(pending_account)
var funded_account = halfyearly_bar.map((item) => item.funded_account);
funded_account=Object.values(funded_account)
var splneAreaColors = getChartColorsArray("#spline_area");
var options = {
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false,
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    series: [{
        name: 'Live Account',
        data: live_account
    }, {
        name: 'Pending Account',
        data: pending_account
    },
    {
        name: 'Funded Account',
        data: funded_account

    }],
    colors: splneAreaColors,
    xaxis: {
        type: 'month',
        categories: month,                
    },
    grid: {
        borderColor: '#f1f1f1',
    },
    tooltip: {
        x: {
            format: 'MM'
        },
    }
}

var chart = new ApexCharts(
    document.querySelector("#spline_area"),
    options
);



chart.render();

// Bar chart
var barColors = getChartColorsArray("#bar_chart_ticketsprocessed");
var options = {
    chart: {
        height: 350,
        type: 'bar',
        toolbar: {
            show: false,
        }
    },
    plotOptions: {
        bar: {
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    series: [{
        data: []
    }],
    colors: barColors,
    grid: {
        borderColor: 'transparent',
    },
    xaxis: {
        categories: [],
    }
}

var chart = new ApexCharts(
    document.querySelector("#bar_chart_ticketsprocessed"),
    options
);
chart.render();










