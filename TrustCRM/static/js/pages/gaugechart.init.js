
var gaugeval=0
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
function gauge1(gaugeval){

        /* gauge chart leadscore */
        if(gaugeval=='undefined'){
            gaugeval=0
        }
       
        var gaugeColors = getChartColorsArray("#gauge-chart-leadscore");
        var dom = document.getElementById("gauge-chart-leadscore");
        var myChart = echarts.init(dom);
        var app = {};
        option = null;
        option = {
            
        
            tooltip : {
                formatter: "{a} <br/>{b} : {c}%"
            },
            toolbox: {
            show: false,
            },
            

            series: [
                {
                    name: 'Lead score',
                    type: 'gauge',
                    detail: {formatter:'{value}%'},
                   
                    margin: [0, 0, 0, 0],
                    spacing: [0, 0, 0, 0],
                
                    axisLine: {   
                        length:8,  
                        show: false,
                        lineStyle: {       
                            color: [[1, gaugeColors[0]]],  //,[0.8, gaugeColors[1]],[1, gaugeColors[2]]
                            width: 8
                        }
                    },
                    splitLine: {
                        length: 15,
                        lineStyle: {
                        width: 1,
                        color: 'rgba(255, 255, 255, 0.2)'
                        }
                    },
                    axisTick: {
                        //distance: -1,
                        length: 10,
                        lineStyle: {
                        color: '#24C38E',  
                        //color: 'rgba(246, 251, 253, 0.1)', 
                        width: 5
                        }
                    },
                    axisLabel: {
                        //distance: 10,
                        color: 'rgba(255, 255, 255, 0.6)',
                        fontSize: 8,
                        fontFamily: 'gilroymedium',
                    },
                    anchor: {
                        show: true,
                        showAbove: true,
                        size: 25,
                        itemStyle: {
                        borderWidth: 10
                        }
                    },
                    detail: {
                    formatter:'{value}%',
                    valueAnimation: true,
                    fontSize: 25,
                    offsetCenter: [0, '70%'],
                    color:'#fff'
                    },
                    data: [{value:gaugeval, name: ''}]
                }
            ]
    };

    // setInterval(function () {
    //     option.series[0].data[0].value = 0;
    //     myChart.setOption(option, true);
    // },2000);
    ;
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}

gauge1(gaugeval);    

var colorvalue=0
var values=0
function gauge2(values){

        /* gauge chart leadscore */
        console.log("Values-------"+values)
        if(values=='undefined'){
            values=0
            colorvalue=0
        }
        colorvalue=values/100
        var gaugeColors1 = getChartColorsArray("#gauge-chart-meetingsscore");
        var dom1 = document.getElementById("gauge-chart-meetingsscore");
        var myChart1 = echarts.init(dom1);
        var app = {};
        option1 = null;
        option1 = {
            
        
            tooltip : {
                formatter: "{a} <br/>{b} : {c}%"
            },
            toolbox: {
            show: false,
            },
            series: [
                {
                    name: 'Lead score',
                    //startAngle: 180,
                    //endAngle: 0,
                    type: 'gauge',
                    detail: {formatter:'{value}%'},
                
                    //0.5
                
                    axisLine: {   
                        length:8,  
                        show: true,
                        lineStyle: {       
                            color: [[colorvalue, gaugeColors1[0]],[1, gaugeColors1[1]]],  //,[0.8, gaugeColors[1]],[1, gaugeColors[2]]
                            width: 8
                        }
                    },
                    pointer: {
                        show: false,
                        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                        length: '12%',
                        width: 20,
                        offsetCenter: [0, '-60%'],
                        itemStyle: {
                          color: 'auto'
                        }
                      },
                    splitLine: {
                        show: false,
                        /*length: 15,
                        lineStyle: {
                        width: 1,
                        color: 'rgba(255, 255, 255, 0.2)'
                        }*/
                    },
                    axisTick: {
                        show: false,
                        //distance: -1,
                        /*length: 10,
                        lineStyle: {
                        color: '#24C38E',  
                        //color: 'rgba(246, 251, 253, 0.1)', 
                        width: 5
                        }*/
                    },
                    axisLabel: {
                        show: false,
                        //distance: 10,
                        /*color: 'rgba(255, 255, 255, 0.6)',
                        fontSize: 8,
                        fontFamily: 'gilroymedium',*/
                    },
                    anchor: {
                        show: true,
                        showAbove: true,
                        size: 25,
                        itemStyle: {
                            borderWidth: 10
                        }
                    },
                    detail: {
                    formatter:'{value}%',
                    valueAnimation: true,
                    fontSize: 25,
                    offsetCenter: [0, '0%'],
                    color:'#fff'
                    },
                    data: [{value:values, name: ''}]
                }
            ]
    };
/*
    setInterval(function () {
        option1.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;
        myChart1.setOption(option1, true);
    },2000);
    ;*/
    if (option1 && typeof option1 === "object") {
        myChart1.setOption(option1, true);
    }
}
gauge2(values);