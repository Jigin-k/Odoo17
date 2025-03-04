/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useState, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class CybroDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.state = useState({
            metrics_data: [],
            tiles_data:[],
            month_year_options: [],
            metricsFilter: '',
            startDate:'',
            endDate:'',
            selectedMonthYear:'',
            lineMetricsFilter:'',
            isDatePickerVisible: false,
            selectedDate: false,
            comparisonData: {},
            lineChartData:{}
        });
        this.chartRef = useRef("chartRef");
        this.lineChartRef = useRef("lineChartRef");
        this.chartInstance = null;
        this.lineChartInstance = null;

        onWillStart(async () => {
            await this._load_tiles_data();
//            await this.loadMonthYearOptions();
            await this._metrics_data();
            await this.onSubmitCompareDateClick();

        });

    }

    onCompareButtonClick() {
        this.state.isDatePickerVisible = true;
    }

    async onSubmitCompareDateClick() {
          console.log("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        try {
            const result = await this.orm.call("cybro.stats", "get_compared_field_values",[]);
            this.state.comparisonData = result;
            this.renderBarGraph();
        } catch (error) {
            console.error("Error fetching comparison data:", error);
        }
    }

    onDateChange(event) {
        this.state.selectedDate = event.target.value;
    }

    onMetricChange(event) {
        this.state.metricsFilter = event.target.value;
        this.renderBarGraph();
    }

    async onMetricsChange() {
    const StartDate = this.state.startDate;
    const EndDate = this.state.endDate;
    const SelectedMetric = this.state.lineMetricsFilter;
    try {
            const result = await this.orm.call("cybro.stats", "get_metrics_period_data", [StartDate,EndDate,SelectedMetric]);
            this.state.lineChartData = result;
            this.renderLineGraph();
        } catch (error) {
            console.error("Error fetching comparison data:", error);
        }

    }

    async _load_tiles_data(){
         this.state.tiles_data = await this.orm.call("cybro.stats","get_tiles_data",[])
    }

//    async loadMonthYearOptions() {
//                this.state.month_year_options = await this.orm.call('cybro.stats','get_distinct_months_years',[])
//        }

    async _metrics_data() {
        this.state.metrics_data = await this.orm.call("cybro.stats", "get_all_field_values",[]);
    }

    renderBarGraph() {
    if (!this.chartRef.el || !this.state.metricsFilter) {
        console.warn("Canvas element not available yet or no metric selected.");
        return;
    }

    if (this.chartInstance) {
        this.chartInstance.destroy();
    }

    const ctx = this.chartRef.el.getContext('2d');
    const metricName = this.state.metricsFilter;
    const currentValue = this.state.metrics_data[metricName] || 0;
    const comparisonValue = this.state.comparisonData[metricName] || 0;

    this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Metric Comparison'],
            datasets: [
                {
                    label: 'Current Value',
                    data: [currentValue],
                    backgroundColor: ["#003f5c"],
                    borderWidth: 1
                },
                {
                    label: 'Comparison Value',
                    data: [comparisonValue],
                    backgroundColor: ["#ff7c43"],
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: metricName,
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'top',
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            barPercentage: 0.6,
            categoryPercentage: 0.8,
            layout: {
                padding: {
                    left: 10,
                    right: 10
                }
            }
        }
    });
}

    renderLineGraph() {
    if (!this.lineChartRef.el || !this.state.lineMetricsFilter) {
        console.warn("Canvas element not available yet or no metric selected.");
        return;
    }

    if (this.lineChartInstance) {
        this.lineChartInstance.destroy();
    }

    const ctx = this.lineChartRef.el.getContext('2d');
    ctx.clearRect(0, 0, this.lineChartRef.el.width, this.lineChartRef.el.height);

    this.lineChartRef.el.width = this.lineChartRef.el.offsetWidth;
    this.lineChartRef.el.height = 300; // Adjust height as needed

    const labels = Object.keys(this.state.lineChartData);
    const data = Object.values(this.state.lineChartData);

    this.lineChartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: this.state.lineMetricsFilter,
                backgroundColor: [
                    "#003f5c", "#2f4b7c", "#f95d6a", "#665191",
                    "#d45087", "#ff7c43", "#ffa600", "#a05195",
                    "#6d5c16", "#CCCCFF"
                ],
                borderColor: "#003f5c",
                data: data,
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: this.state.lineMetricsFilter,
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10
                }
            }
        }
    });
}

}

CybroDashboard.template = "cybro_stats.CybroDashboard";
actionRegistry.add("cybro_dashboard_tag", CybroDashboard);