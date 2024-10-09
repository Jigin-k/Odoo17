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
         this.state = useState({
            countDictionary : [],
            op_types: [],
            operations: [],
            colors: [],
            late_status: [],
            waiting_status: [],
            backorder_status: [],
            MoveData: [],
            operationDict: [],
            category: [],
            categCountDict: [],
            categName: [],
            location_data: [],
            monthly_stock: [],
            monthly_stock_count: [],
            out_stock: [],
            out_stock_count: [],
            dead_stock_name: [],
        });
        this._inventory_data()
        this._storage_location()
        this.chart = null;

        onWillStart(async () => await loadBundle("web.chartjs_lib"));
        useEffect(() => {
//            this.barChart();
//            this.pieChart();
//            this.doughnutChart();
//            this.lineChart();
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
        this.orm.call("stock.picking", "get_locations",
        ).then((result) => {
            this.state.location_data = result
        });
    }

}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
