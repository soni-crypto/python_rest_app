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

var options_apx_bar = {
    series: [{
    data: [],
    name: "Cantidad",
}],
    chart: {
    type: 'bar',
    height: 350
},
colors: colors,
plotOptions: {
    bar: {
    borderRadius: 4,
    borderRadiusApplication: 'end',
    horizontal: true,
    distributed: true,
    }
},
dataLabels: {
    enabled: false
},
xaxis: {
    categories: [],
}
};
fetch("/honey/reports-admin?for=apex&mode_filter="+ String(document.getElementById("mode_filter").value)).then(res => res.json()).then(data=>{
    if (data[0]){
        data[0][1].forEach((a)=>{
            options_apx_bar.series[0].data.push(a.quantity_category);
            options_apx_bar.xaxis.categories.push(a.category_name);
        })
    }
    var chart = new ApexCharts(document.querySelector("#chart-2"), options_apx_bar);
    chart.render();
});



