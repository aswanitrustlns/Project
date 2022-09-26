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
    return colors.map(function (value) {
        var newValue = value.replace(' ', '');
        if (newValue.indexOf('--') != -1) {
            var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
            if (color) return color;
        } else {
            return newValue;
        }
    })
}
function renderChart($series, $id, $catogories) {

    //column chart1  New Accounts
    var columnColors = getChartColorsArray($id);
    var options = {
        chart: {
            height: 120,
            type: 'bar',
            toolbar: {
                show: false,
            },
            events: {
                legendClick: function(chartContext, seriesIndex, config) {
                   //console.log('chartConfigId', chartContext.el.id.split("-")[2]);
                   //console.log('seriesIndex', seriesIndex);
                   //console.log(chartContext);
                   if(seriesIndex==0){
                    loadClosed()
                   }else if(seriesIndex==1){
                    loadOpen()
                   }
                 
                 
                }
            },
           
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
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false,
            },

            labels: {
                trim: true,

                rotate: -45,
                rotateAlways: false,
                hideOverlappingLabels: true,
                maxHeight: 60,

                style: {
                    //colors: '#5B5B5B',
                    fontSize: '12px',
                    fontFamily: 'gilroymedium',

                    //cssClass: 'gilroymedium-type text-muted',
                },
            }
        },
        yaxis: {


            show: false,

        },
        grid: {
            borderColor: '#f1f1f1',
            yaxis: {
                lines: {
                    show: false
                }
            },
        },
        fill: {
            opacity: 1

        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return + val + " "
                }
            }
        },
        legend: {
            show: true,
            position: 'top',
            horizontalAlign: 'right',
            verticalAlign: 'center',
            floating: true,
            fontSize: '14px',
            fontFamily: 'gilroymedium',
            offsetY: -0,

            itemMargin: {

                vertical: 0,
            },
        },
        noData: {

            text: 'No Tickets',
    
            align: "center",
            verticalAlign: "middle",
    
            style: {
                color: undefined,
                fontSize: '14px',
                fontFamily: 'giloryregular',
            },
    
    
        },
        responsive: [{
            breakpoint: 600,
            options: {
                chart: {
                    height: 150,
                }

            }
        },
        {
            breakpoint: 1200,
            options: {
                chart: {
                    height: 150,
                }

            }
        },
        {
            breakpoint: 1550,
            options: {
                chart: {
                    height: 220,
                },
            },
        }


        ]
    }

    var chart = new ApexCharts(
        document.querySelector($id),
        options
    );

    chart.render();

}
//rerenderChart($series,$time);
var opens=weekly_lead_bar.map((item) => item.open);
var clos=weekly_lead_bar.map((item) => item.closed);

console.log("closed------------------",clos)
renderChart([{

    name: 'Closed',
    data: clos,
},
{

    name: 'Open',
    data: opens,
},

], '#column_chart_new_accounts', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']);


function switchtab($this, $displaytab, $hiddentab) {
    console.log("switch tab clicked -------------------------------------------")
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

// Donut chart Tickets
var spoken_d=Object.values(ticket_count_daily)[1];
var overdue_d=Object.values(ticket_count_daily)[2];
var resolved_d=Object.values(ticket_count_daily)[3];
var spoken_w=Object.values(ticket_count_weekly)[1];
var overdue_w=Object.values(ticket_count_weekly)[2];
var resolved_w=Object.values(ticket_count_weekly)[3];


function ticketDonut($id,$spoken,$overdue,$resolved){

var donutColors = getChartColorsArray($id);
console.log("iddddddddddddddddddddddddddddddd",$id)

var options = {
    dataLabels: {
        enabled: false,
    },
    plotOptions: {
        pie: {
            expandOnClick: false,
        }
    },
    chart: {

        height: 120,
        //width: 186,
        type: 'donut',
        verticalAlign: 'left',
        horizontalAlign: 'left',
        events: {
            legendClick: function(chartContext, seriesIndex, config) {
               //console.log('chartConfigId', chartContext.el.id.split("-")[2]);
               //console.log('seriesIndex', seriesIndex);
               //console.log(chartContext);
               console.log("Seriesssss Index"+seriesIndex)
               if(seriesIndex==0){
                spokenpageRedirect()
               }else if(seriesIndex==1){
                overduepageRedirect()
               }
               else if(seriesIndex==2){
                resolvepageRedirect()
               }
             
            }
        },
    },
    stroke: {
        show: false,
        width: 0
    },
    series: [$spoken,$overdue,$resolved],
    labels: ['Spoken', 'Overdue', 'Resolved'],
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

        text: 'No Tickets',

        align: "center",
        verticalAlign: "middle",

        style: {
            color: undefined,
            fontSize: '14px',
            fontFamily: 'giloryregular',
        },


    },
    responsive: [

        {
            breakpoint: 1550,
            options: {
                chart: {
                    height: 220,
                },
                legend: {
                    fontSize: '11px!important',


                    position: 'bottom'
                },
            },


        },
        {
            breakpoint: 1200,
            options: {
                chart: {
                    height: 150,
                },
                legend: {
                    fontSize: '11px!important',


                    position: 'bottom'
                },
            },


        },
        {
            breakpoint: 600,
            options: {
                chart: {
                    height: 150,
                },
                legend: {

                    position: 'bottom'
                },
            }
        }


    ]

}
var chart = new ApexCharts(document.querySelector($id), options);
chart.render();
}

ticketDonut("#tickets_tab01",spoken_d,overdue_d,resolved_d);
ticketDonut("#tickets_tab02",spoken_w,overdue_w,resolved_w);
//   spline_area_new_accounts
var funded=weekly_summary.map((item) => item.funded);
var nonfunded=weekly_summary.map((item) => item.nonfunded);
var temprory=weekly_summary.map((item) => item.temp);
var waiting=weekly_summary.map((item) => item.waiting);
console.log("Type of funded-------"+funded.length)
fun_sum=data_sum(funded)


var splneAreaColors = getChartColorsArray("#spline_area_new_accounts");
var options = {
    chart: {
        height: 380,
        type: 'area',
        toolbar: {
            show: false,
        },
        events: {
            legendClick: function(chartContext, seriesIndex, config) {
               //console.log('chartConfigId', chartContext.el.id.split("-")[2]);
               //console.log('seriesIndex', seriesIndex);
               //console.log(chartContext);
               console.log("Seriesssss Index"+seriesIndex)
               if(seriesIndex==0){
                pageRedirect("Funded")
                
               }else if(seriesIndex==1){
                pageRedirect("NonFunded")
               }
               else if(seriesIndex==2){
                pageRedirect("TempApproved")
                
               }
               else if(seriesIndex==3){
                pageRedirect("WaitingApproval")
                
               }

             
            }
        },
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
        width: 4,
    },
    series: [{
        name: 'Funded',
        data: funded
    }, {
        name: 'Non Funded',
        data: nonfunded
    }, {
        name: 'Approved Temporarily',
        data: temprory
    }, {
        name: 'Waiting for approval',
        data: waiting
    },],
    colors: splneAreaColors,
    xaxis: {
        type: ' ',
        categories: ["Mon", "Tue", "Wed", "Thu", "Fri"],

        labels: {


            style: {
                colors: ['#73759D', '#73759D', '#73759D', '#73759D', '#73759D', '#73759D'],
                fontSize: '14px',
                fontFamily: 'gilroymedium ',
                //fontWeight: 400,
                cssClass: 'apexcharts-xaxis-label',
            },


        },
    },
    yaxis: {
        labels: {


            style: {
                colors: ['#73759D', '#73759D', '#73759D', '#73759D', '#73759D', '#73759D'],
                fontSize: '12px',
                fontFamily: 'gilroymedium ',
                //fontWeight: 400,
                cssClass: 'apexcharts-yaxis-label',
            },


        },

    },
    grid: {

        //show: true,

        borderColor: '#333550',

        strokeDashArray: 7, 
     

    },


    legend: {
        show: true,
        showForSingleSeries: true,
        showForNullSeries: true,
        showForZeroSeries: true,
        position: 'bottom',
        horizontalAlign: 'center',
        floating: false,
        fontSize: '14px',
        fontFamily: 'gilroymedium',
        formatter: undefined,
        inverseOrder: false,
        width: undefined,
        height: undefined,
        tooltipHoverFormatter: undefined,
        customLegendItems: [],
        offsetX: 0,
        offsetY: 0,
        labels: {
            colors: ["#73759D", "#73759D", "#73759D", "#73759D", "#73759D"],
            useSeriesColors: false
        },
        markers: {
            width: 12,
            height: 12,
            strokeWidth: 0,
            strokeColor: '#fff',
            fillColors: undefined,
            radius: 12,
            customHTML: undefined,
            onClick: undefined,
            offsetX: 0,
            offsetY: 0
        },
        itemMargin: {
            horizontal: 20,
            vertical: 10,
        },
        onItemClick: {
            toggleDataSeries: true
        },
        onItemHover: {
            highlightDataSeries: true
        }
    },
    tooltip: {
        x: {
            //format: 'dd/MM/yy HH:mm'
        },
    },
   
    responsive: [{
        breakpoint: 1550,
        options: {
            chart: {
                height: 420,
            },
            legend: {
                itemMargin: {
                    horizontal: 5,
                    vertical: 10,
                },

            }
        },
    },
    {
        breakpoint: 1200,
        options: {
            chart: {
                height: 240,
            }

        }
    },
    {
        breakpoint: 600,
        options: {
            chart: {
                height: 200,
            }

        }
    }





    ]

}

var chart = new ApexCharts(
    document.querySelector("#spline_area_new_accounts"),
    options
);



chart.render();



function data_sum(ar) {
    var sum = 0;
    for (var i = 0; i < ar.length; i++) {
      if(typeof ar[i] == `number`) sum += ar[i];
    }
    console.log("Data sum-----------------------"+sum)
    return sum;
  }










