jQuery(document).ready(() => {

    am4core.ready(function() {
        new Vue({
            el: '#filters',
            delimiters:['${', '}'],
            data() {
                return {
                    date_from: "",
                    date_to: "",
                    mode: 'months',
                    chart: null
                }
            },
            filters: {
                date(date) {
                    return moment(date).format('DD/MM/YYYY')
                }
            },
            methods: {
                refreshData() {

                var app = this;
                var url = new URL(window.location.origin + '/rest/report/' + this.mode),
                                        params = {from: moment(this.date_from).format('YYYY-MM-DD'), to: moment(this.date_to).format('YYYY-MM-DD')};
                                    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
                                    fetch(url).then(resp => resp.json()).then(allData => {

                                        data = allData.data;

                                        app.date_from = allData.date_from;
                                        app.date_to = allData.date_to;


                                        let format_moment = 'YYYY-MM-DD';
                                        let format_amcharts = 'yyyy-MM-dd';
                                        if (app.mode == 'months') {
                                            format_moment = 'YYYY-MM';
                                            format_amcharts = 'yyyy-MM';
                                        }

                                        data = data.map(datum => {
                                            return {
                                                date: moment(datum[0]).format(format_moment),
                                                value: datum[1]
                                            }
                                        })
                                        console.log(data);


                                         // Themes begin
                                                                        am4core.useTheme(am4themes_animated);
                                                                        // Themes end

                                                                        // Create chart instance
                                                                        var chart = am4core.create("report", am4charts.XYChart);

chart.language.locale = am4lang_es_ES;
                                                    chart.data = data;
                                                                        // Set input format for the dates
                                                                        chart.dateFormatter.inputDateFormat = format_amcharts;

                                                                        // Create axes
                                                                        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                                                                        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

                                                                        // Create series
                                                                        var series = chart.series.push(new am4charts.LineSeries());
                                                                        series.dataFields.valueY = "value";
                                                                        series.dataFields.dateX = "date";
                                                                        series.tooltipText = "{value}"
                                                                        series.strokeWidth = 2;
                                                                        series.minBulletDistance = 15;

                                                                        // Drop-shaped tooltips
                                                                        series.tooltip.background.cornerRadius = 20;
                                                                        series.tooltip.background.strokeOpacity = 0;
                                                                        series.tooltip.pointerOrientation = "vertical";
                                                                        series.tooltip.label.minWidth = 40;
                                                                        series.tooltip.label.minHeight = 40;
                                                                        series.tooltip.label.textAlign = "middle";
                                                                        series.tooltip.label.textValign = "middle";

                                                                        // Make bullets grow on hover
                                                                        var bullet = series.bullets.push(new am4charts.CircleBullet());
                                                                        bullet.circle.strokeWidth = 2;
                                                                        bullet.circle.radius = 4;
                                                                        bullet.circle.fill = am4core.color("#fff");

                                                                        var bullethover = bullet.states.create("hover");
                                                                        bullethover.properties.scale = 1.3;

                                                                        // Make a panning cursor
                                                                        chart.cursor = new am4charts.XYCursor();
                                                                        chart.cursor.behavior = "panXY";
                                                                        chart.cursor.xAxis = dateAxis;
                                                                        chart.cursor.snapToSeries = series;

                                                                        // Create vertical scrollbar and place it before the value axis
                                                                        chart.scrollbarY = new am4core.Scrollbar();
                                                                        chart.scrollbarY.parent = chart.leftAxesContainer;
                                                                        chart.scrollbarY.toBack();

                                                                        // Create a horizontal scrollbar with previe and place it underneath the date axis
                                                                        chart.scrollbarX = new am4charts.XYChartScrollbar();
                                                                        chart.scrollbarX.series.push(series);
                                                                        chart.scrollbarX.parent = chart.bottomAxesContainer;

                                                                        dateAxis.start = 0.79;
                                                                        dateAxis.keepSelection = true;

                })
                }
            },
            mounted() {
                this.date_from = moment().subtract(7, 'days').format('YYYY-MM-DD')

                if (this.mode == 'months') {
                    this.date_from = moment().subtract(6, 'months').format('YYYY-MM-DD')
                }
                this.date_to = moment().format('YYYY-MM-DD')
                this.refreshData()
            }
        })
    }); // end am4core.ready()
})
