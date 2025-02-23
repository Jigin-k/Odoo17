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
            metricsFilter: '',
            startDate:'',
            endDate:'',
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
            await this._metrics_data();
        });

//        onMounted(() => {
//            this.renderBarGraph();
//        });
    }

    onCompareButtonClick() {
        this.state.isDatePickerVisible = true;
    }
//
//    onCancelCompareDateClick() {
//        this.state.isDatePickerVisible = false;
//    }

    async onSubmitCompareDateClick() {
        const selectedDate = this.state.selectedDate;

        try {
            const result = await this.orm.call("cybro.stats", "get_compared_field_values", [selectedDate]);
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
    async onApplyDateClick() {
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

    async _metrics_data() {
        this.state.metrics_data = await this.orm.call("cybro.stats", "get_all_field_values", [this.props.action.context.active_id]);
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
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Comparison Value',
                    data: [comparisonValue],
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
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

        // Destroy existing chart instance if it exists
        if (this.lineChartInstance) {
            this.lineChartInstance.destroy();
        }

        const ctx = this.lineChartRef.el.getContext('2d');
        const labels = Object.keys(this.state.lineChartData)
        const data = Object.values(this.state.lineChartData)
        this.lineChartInstance = new Chart(ctx, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            backgroundColor: [
                            "#003f5c","#2f4b7c","#f95d6a","#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
            data: data
        }]
    },
    options: {
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
    }
      });
    }

}

CybroDashboard.template = "cybro_stats.CybroDashboard";
actionRegistry.add("cybro_dashboard_tag", CybroDashboard);