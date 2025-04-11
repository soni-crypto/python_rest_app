var _seed = 42;
Math.random = function() {
    _seed = _seed * 16807 % 2147483647;
    return (_seed - 1) / 2147483646;
};
var colors = [
    '#008FFB',
    '#00E396',
    '#FEB019',
    '#FF4560',
    '#775DD0',
    '#546E7A',
    '#26a69a',
    '#D10CE8',

    '#3b9d12',
    '#283343',
    '#7e9c0d',
    '#710df7',
    '#cee8ba',
    '#b937b6',
    '#c86ad2',
    '#7d0020',
    '#41ff00',
    '#ff0000',
    '#1f8e8a',
]
var options_apx = {
        series: [{
        data: [],
        name:"Cantidad",
    }],
        chart: {
        height: 350,
        type: 'bar',
        events: {
        click: function(chart, w, e) {
            // console.log(chart, w, e)
        }
        }
    },
    colors: colors,
    plotOptions: {
        bar: {
        columnWidth: '80%',
        distributed: true,
        }
    },
    dataLabels: {
        enabled: false,
    },
    legend: {
        show: false,
    },
    xaxis: {
        categories: [
        // ['Salchipa especial', 'otro nombre'],
        ],
        labels: {
        style: {
            colors: colors,
            fontSize: '10px',
        },
        }
    }
};
fetch("/honey/reports-admin?for=apex&mode_filter="+ String(document.getElementById("mode_filter").value)).then(res => res.json()).then(data=>{
    if (data[0]){
        data[0][0].forEach((a)=>{
            options_apx.series[0].data.push(a.quantity_food);
            options_apx.xaxis.categories.push(a.food_name);
        })
    }
    var chart = new ApexCharts(document.querySelector("#chart-1"), options_apx);
    chart.render();
});
