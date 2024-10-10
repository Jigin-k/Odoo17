/**@odoo-module **/
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useState, useRef } from "@odoo/owl";

import { Component, onWillStart, useEffect } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class InventoryDashboard extends Component {
    setup() {
        super.setup()
        this.orm = useService('orm')
        this.rootRef = useRef('root')
         this.state = useState({
            location_data: [],
            StockData: [],
        });
        this._inventory_data()
        this._storage_location()
        this._stock_location_pie_chart()
        this.chart = null;

        onWillStart(async () => await loadBundle("web.chartjs_lib"));
        useEffect(() => {
        this._product_average_expense_graph()
        });
    }

    async _inventory_data() {
        await this.orm.call("stock.picking", "get_inventory_tiles_data", [], {}).then(function (result) {
            $('#incoming_operations').append('<span>' + result.incoming_operations + '</span>');
            $('#outgoing_operations').append('<span>' + result.outgoing_operations + '</span>');
            $('#internal_transfers').append('<span>' + result.internal_transfers + '</span>');
        });
    }
     async _storage_location(){
        await this.orm.call("stock.picking", "get_locations",
        ).then((result) => {
            this.state.location_data = result
        });
    }
    _product_average_expense_graph() {
    // Call the ORM method to get average expense data
    this.orm.call("stock.picking", "get_average_expense", []
    ).then((result) => {
    console.log(result)
    var product_names = Object.keys(result);
        console.log(product_names)
    var avg_price = Object.values(result)
        console.log(avg_price)
    var ctx = $('#canvas_bar')
    if (this.chart){
    this.chart.destroy();
    }
    this.chart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: product_names,
        datasets: [{
            backgroundColor: [
                            "#003f5c","#2f4b7c","#f95d6a","#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
            data: avg_price
        }]
    },
    options: {}
      });
    })
   }
    async _stock_location_pie_chart(){
        this.orm.call("stock.move", "get_stock_moves", []
        ).then( (result) => {
            console.log(result)
            var name = result.name
            var count = result.count;
            var stockMoveDict = {}
            for (var i = 0; i < name.length; i++) {
                var location = name[i];
                var stockCount = count[i];
                stockMoveDict[location] = stockCount;
            }
            this.state.StockData = stockMoveDict;
            console.log(this.state.StockData)
            var ctx = $('#canvas_pie')
            var myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: name,
                    datasets: [{
                        label: 'Count',
                        data: count,
                        backgroundColor: [
                            "#003f5c","#2f4b7c","#f95d6a","#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
                        barThickness: 6,
                        type: 'pie',
                        fill: false
                    }]
                },
                options: {
                }
            });
        });
    }
}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
