/*
Template Name: Minia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Dashboard Init Js File
*/

//const { removeData } = require("jquery");

// get colors array from the string
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


// Donut chart #meetings_report
var data_d = meeting_daily_pie.map((item) => item.value);

// data_d=Object.values(data_d)

var username_d = meeting_daily_pie.map((item) => item.name);
// username_d=Object.values(username_d)
var data_w = meeting_weekly_pie.map((item) => item.value);
console.log(data_w)
data_w=Object.values(data_w)
console.log(data_w)
var username_w = meeting_weekly_pie.map((item) => item.name);
console.log(username_w)
username_w=Object.values(username_w)
console.log(username_w)

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
      height: '100%',
      type: 'donut',
      verticalAlign: 'left',
  }, 
  stroke: {
    show: false,
    width: 0
    },
  series: $series,
  labels: $label,
  colors: donutColors,
  legend: {
        show: true,
        position: 'right',
        horizontalAlign: 'left',
        verticalAlign: 'center',
        floating: false,
        fontSize: '14px!important',
        fontFamily: 'gilroymedium',
        offsetX: 0,

      itemMargin: {
        
        vertical: 4,
    },
  },
  noData: {
        
    text:'Nothing to display',
    align: "center",
    verticalAlign: "middle",
    
    style: {
        color: undefined,
        fontSize: '14px',
        fontFamily: 'giloryregular',
    },
   
    
},
  responsive: [{
      breakpoint: 1550,
      options: {
          chart: {
              height: '110%',
          },
          legend: {
              
              position: 'bottom',
              verticalAlign: 'left',
              floating: false,
              offsetX: 0,
              offsetY: 0,
              itemMargin: {
        
                vertical: 1,
                horizontal: 4,
            },
          },
      }
  },

  {
    breakpoint: 1350,
    options: {
        chart: {
        },
        legend: {
            offsetX: 0,
            offsetY: 0,
            fontSize: '11px!important',     
            position: 'bottom'
        },
    },
}


]

}
var chart = new ApexCharts(
  document.querySelector($id),
  options
);
chart.render()
}
renderMeetingDonut(data_d,"#meetings_report_d",username_d)
renderMeetingDonut(data_w,"#meetings_report_w",username_w)
// column chart2 liveaccount_statics
var columnColors = getChartColorsArray("#column_chart_leadsbysource");
var src_count = leads_graph.map((item) => item.src_count);
var ticket_count = leads_graph.map((item) => item.ticket_count);
var graph_name =leads_graph.map((item) => item.name);
var options = {
    chart: {
        height: '110%',
        type: 'bar',
        toolbar: {
            show: false,
        }
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '25',  
        },
    },
    dataLabels: {
        enabled: false,
    },
    stroke: {
        show: false,
        width: 2,
        colors: ['transparent']
    },
    series: [{
        name: 'Source Count',
        data: src_count
        }, {
        name: 'Ticket Count',
        data: ticket_count
        }
    ],
    colors: columnColors,
    xaxis: {

        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false,
        },
        lines: {
            
            show: true,
            opacity: 0.5,
        },    
    categories: graph_name,

    labels: {
        trim: true,
        rotate: -20,
        rotateAlways: false,
        hideOverlappingLabels: true,
        maxHeight: 80,
        style: {
            
            fontSize: '12px',
            fontFamily: 'gilroyregular',
           
        },
    },
  
    },
    yaxis: {
        lines: {
            show: false,
        }
    },
    grid: {
        borderColor: '#333550',
        strokeDashArray: 7,
    
    },
    legend: {
        show: true,
        position: 'bottom',
        horizontalAlign: 'center',
        verticalAlign: 'center',
        fontSize: '14px',
        
        fontFamily: 'gilroymedium',
        offsetY: -10,

        itemMargin: {

            vertical: 0,
            horizontal: 10,
        },
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
    },

    responsive: [{
        breakpoint: 1400,
        options: {
            chart: {
                height: '100%',
            }

        }
    },
    {
        breakpoint: 1200,
        options: {
            chart: {
                height: '110%',
            }

        }
    },



],
}
var chart = new ApexCharts(
    document.querySelector("#column_chart_leadsbysource"),
    options
);
chart.render();

// weekly-seminar #weekly-seminar


var seminar_data_d = seminar_daily_pie.map((item) => item.value);
var seminar_username_d = seminar_daily_pie.map((item) => item.name);
seminar_username_d=Object.values(seminar_username_d)

var seminar_data_w = seminar_weekly_pie.map((item) => item.value);
var seminar_username_w = seminar_weekly_pie.map((item) => item.name);
seminar_username_w=Object.values(seminar_username_w)


function renderSeminarPie($series,$id,$label){

var piechartColors = getChartColorsArray($id);
var options = {
    series: $series,
    labels: $label,
    colors: piechartColors,
    chart: {
        height: '100%',
        type: 'pie',
        verticalAlign: 'left',
        horizontalAlign: 'left',

        events: {
            legendClick: function(chartContext, seriesIndex, config) {
      
               if(seriesIndex==0){
                window.open("https://www.w3schools.com");
               }else if(seriesIndex==1){
                    window.open("https://trusttc.com");
               }
               else if(seriesIndex==2){
                window.open("https://trustcapitaltc.eu");
               }
             
            }
        }
    },

    xaxis: {
        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false,
        },
        lines: {
            show: false,
            opacity: 0,
        },
                        
    },
    stroke: {
        width: 0,
    },
    legend: {
        show: true,
        position: 'right',
        horizontalAlign: 'left',
        verticalAlign: 'center',
        floating: false,
        fontSize: '14px!important',
        fontFamily: 'gilroymedium',
        offsetX: 0,
        itemMargin: {
            vertical: 4,
        },
    },
    dataLabels: {
        enabled:true,
        formatter: function (val) {
            return Math.trunc(val) + "%"
        },
        enabledOnSeries: undefined,
        textAnchor: 'middle',
        distributed: false,
        offsetX: 0,
        offsetY: 0,
        style: {
            fontSize: '12px !important',
            fontFamily: 'giloryregular',
        },
        dropShadow: {
            enabled: false,
            top: 0,
            left: 0,
            blur: 0,
            color: 'transparent',
            opacity: 0.45
        }
    },
    noData: {
        
        text:'Nothing to display',
        align: "center",
        verticalAlign: "middle",

        style: {
            color: undefined,
            fontSize: '14px',
            fontFamily: 'giloryregular',
        },
       
        
    },
   //Responsive
    responsive: [{
        breakpoint: 1550,
        options: {
            chart: {
            
                height: '120%',
            },
            legend: {
                show: true,
                position: 'bottom',
                horizontalAlign: 'center',
                verticalAlign: 'center',
                floating: false,
                fontSize: '14px!important',
                fontFamily: 'gilroymedium',
                offsetY: 0,
                itemMargin: {
                    vertical: 1,
                    horizontal: 4,
                },
            },
        }
    },
    {
        breakpoint: 1400,
        options: {
            chart: {
            
                height: '100%',
            },
            legend: {
                show: true,
                position: 'right',
                horizontalAlign: 'center',
                verticalAlign: 'center',
                floating: false,
                fontSize: '14px!important',
                fontFamily: 'gilroymedium',
                offsetY: 0,
                itemMargin: {
                    vertical: 4,
                    horizontal: 1,
                },
            },
        }
    },
    {
        breakpoint: 1200,
        options: {
            chart: {
            
                height: '130%',
            },
            legend: {
                show: true,
                position: 'bottom',
                horizontalAlign: 'center',
                verticalAlign: 'center',
                floating: false,
                fontSize: '14px!important',
                fontFamily: 'gilroymedium',
                offsetY: 0,
                itemMargin: {
                    vertical:1,
                    horizontal: 4,
                },
            },
        }
    }


    ]

};

var chart = new ApexCharts(document.querySelector($id), options);
chart.render();
}
renderSeminarPie(seminar_data_d,'#weekly-seminar_d',seminar_username_d);
renderSeminarPie(seminar_data_w,'#weekly-seminar_w',seminar_username_w);
// function switchtab($this,$displaytab,$hiddentab) {
//     $($displaytab).addClass('d-block');
 
//     $($displaytab).removeClass('d-none');
//     $($hiddentab).addClass('d-none');
//     $($hiddentab).removeClass('d-block');  
   
    
    
// }


//#spline_area


//function renderChart($id){

    //var chart = new ApexCharts(
        //document.querySelector($id),
        //options
    //);
    
    //chart.render();


//}

var month = halfyearly_bar.map((item) => item.month);
// month=Object.values(month)
var live_account = halfyearly_bar.map((item) => item.live_account);
live_account=Object.values(live_account)
var pending_account = halfyearly_bar.map((item) => item.pending_account);
pending_account=Object.values(pending_account)
var funded_account = halfyearly_bar.map((item) => item.funded_account);
funded_account=Object.values(funded_account)
var tickets=halfyearly_bar.map((item)=>item.tickets);
tickets=Object.values(tickets);
var leads=halfyearly_bar.map((item)=>item.leads);
leads=Object.values(leads);





//   spline_area
var splneAreaColors = getChartColorsArray("#spline_area");
var options = {
    chart: {
        height: '100%',
        type: 'area',
        toolbar: {
            show: false,
        }
    },
    legend:{
        show:false,
    },
    fill: {
        type: "solid",
        opacity: 0,
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

    },
    {
        name: 'Tickets',
        data: tickets

    },
    {
        name: 'Leads',
        data: leads

    }

],
    colors: splneAreaColors,
    xaxis: {
        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false,
        },
        lines: {
            show: false,
            opacity: 0,
        },
        type: 'month',
        categories: month,                
    },
    grid: {
        borderColor: '#333550',
        strokeDashArray: 7,
       
    },
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
    //Responsive    
    responsive: [{
        breakpoint: 1399,
        options: {
            chart: {
            
                height: '100%',
            },
          
        }
    }]
}

var chart = new ApexCharts(
    document.querySelector("#spline_area"),
    options
);
chart.render();
//switchtab
function switchtab($this, $displaytab, $hiddentab) {
    console.log("Dispplay tab-------"+$displaytab)
    console.log("Hidden tab========"+$hiddentab)
    $($displaytab).addClass('d-block');
    $($displaytab).removeClass('d-none');
    $($hiddentab).addClass('d-none');
    $($hiddentab).removeClass('d-block');
    if ($($this).hasClass('bg-soft-gunmetal')) {
    } else {

        $($this).addClass('bg-soft-gunmetal');
        $($this).siblings().removeClass('bg-soft-gunmetal');
    }


}
// $('table').scrollTableBody();













