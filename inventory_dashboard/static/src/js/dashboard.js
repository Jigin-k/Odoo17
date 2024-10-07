/**@odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from  "@odoo/owl";
import { onWillStart, onMounted, useState, useRef } from "@odoo/owl";
const actionRegistry = registry.category("actions");
import { useService } from "@web/core/utils/hooks";
var op_type;
class InventoryDashboard extends Component {
               setup() {
        this.orm = useService('orm')
        this._fetch_data()
        this.state = useState({
            countDictionary : [],
            op_types: [],
             operations: []
            })
        }
        _fetch_data(){
   var self = this;
  this.orm.call("stock.picking", "get_operation_types", [], {}).then(function(result){

  op_type = result[1];
  this.op_types = result[0]
  this.operations = result[1]
  console.log(this.op_types)
  console.log(this.operations)
           });
       };
       };

InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
