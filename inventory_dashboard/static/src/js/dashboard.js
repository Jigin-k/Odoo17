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
        this.rotRef = useRef('root')
         this.state = useState({
            location_data: [],
            StockData: [],
        });
        this._inventory_data()
        this._storage_location()

        this.chart = null;
        this.myChart = null;
        this.productChart = null;
        this.StockValuationChart = null;

        useEffect(() => {
        this._product_average_expense_graph()
        this._stock_location_pie_chart()
        this._product_move_chart()
        this._stock_valuation_chart()

        });
    }

    async _inventory_data() {
        await this.orm.call("stock.picking", "get_inventory_tiles_data", [], {}).then(function (result) {
            document.getElementById('incoming_operations').append(result.incoming_operations);
            document.getElementById('outgoing_operations').append(result.outgoing_operations );
            document.getElementById('internal_transfers').append(result.internal_transfers);
        });
    }
     async _storage_location(){
        await this.orm.call("stock.picking", "get_locations",
        ).then((result) => {
            this.state.location_data = result
            console.log(this.state.location_data,"qqqqq")
        });
    }
    _product_average_expense_graph() {
    this.orm.call("stock.picking", "get_average_expense", []
    ).then((result) => {
    var product_names = Object.keys(result);
    var avg_price = Object.values(result)
    var ctx = document.getElementById('canvas_bar')
    if (this.chart){
    this.chart.destroy();
    }
    this.chart = new Chart(ctx, {
    type: "line",
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
            var name = result.name
            var count = result.count;
//            var stockMoveDict = {}
//            for (var i = 0; i < name.length; i++) {
//                var location = name[i];
//                var stockCount = count[i];
//                stockMoveDict[location] = stockCount;
//            }
//            this.state.StockData = stockMoveDict;
//            console.log(this.state.StockData)
            var ctx = document.getElementById('canvas_pie')
            if (this.myChart){
             this.myChart.destroy();
            6 }
            this.myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: name,
                    datasets: [{
                        label: 'Count',
                        data: count,
                        backgroundColor: [
                            "#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
                        barThickness: 6,
                        type: 'pie',
                        fill: false
                    }]
                },
            });
        });
    }

    async _product_move_chart(){
        this.orm.call("stock.move.line", "get_product_moves", []
        ).then( (result) => {
        var product_names = result.name;
    var move_count = result.count;
    var ctx = document.getElementById('product_move_bar')
    if (this.productChart){
    this.productChart.destroy();
    }
    this.productChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: product_names,
        datasets: [{
            backgroundColor: [
                            "#ff7c43","#2f4b7c","#a05195","#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
            data: move_count
       }]
      },
     });
    });
    }
    async _stock_valuation_chart(){
        this.orm.call("stock.valuation.layer", "get_stock_value", []
        ).then( (result) => {
        console.log(result)
        var product_names = result.name;
        console.log(product_names)
    var stock_value = result.stock_value;
        console.log(stock_value)
    var ctx = document.getElementById('canvas_doughnut')
    if (this.StockValuationChart){
    this.StockValuationChart.destroy();
    }
    this.StockValuationChart = new Chart(ctx, {
    type: "doughnut",
    data: {
        labels: product_names,
        datasets: [{
            backgroundColor: [
                           "#665191",
                            "#d45087","#ff7c43","#ffa600","#a05195",
                            "#6d5c16","#CCCCFF"
                        ],
            data: stock_value
        }]
       },
      });
     });
    }

   async onchange_filter_selection() {
  const option = document.getElementById("filter_selection").value;

  if (option === "this_week" || option === "this_month" || option === "this_year") {
      const result = await this.orm.call("stock.move", "get_filter_product_moves", [option]);

      const ctx = document.getElementById("product_move_bar");

      if (this.productChart) {
        this.productChart.destroy();
      }

      this.productChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: result.name,
          datasets: [
            {
              label: "Count",
              data: result.count,
              backgroundColor: [
                "#003f5c", "#2f4b7c", "#f95d6a", "#665191",
                "#d45087", "#ff7c43", "#ffa600", "#a05195",
                "#6d5c16", "#CCCCFF",
              ],
            },
          ],
        },
      });

  }
  else{
    this._product_move_chart()
  }
}
    redirectToIncoming(){
 this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Incoming',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','incoming'],
                                           ['state', 'not in',
                                            ['done', 'cancel']]]
       });
 }

 redirectToOutgoing(){
 this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Outgoing',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','outgoing'],
                  ['state', 'not in',['done', 'cancel']]]
       });
 }
 redirectToInternalTransfer(){
 this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Internal Transfer',
         res_model: 'stock.picking',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
        domain : [['picking_type_id.code', '=','internal'],
                  ['state', 'not in',['done', 'cancel']]]
       });
 }
RedirectLocation(location){
console.log(location)
 this.env.services.action.doAction({
         type: 'ir.actions.act_window',
         name: 'Location',
         res_model: 'stock.quant',
         views: [[false, "list"], [false, "form"]],
         target: 'current',
           domain : [['location_id.name', '=',location]]
                });
 }




}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
