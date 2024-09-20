/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";


patch(Order.prototype, {
    async pay() {
    console.log(this);
    console.log(this.get_last_orderline());
//(this.orderlines).forEach((el) =>  console.log(el.tax_ids[0]))
//let sum = 0;
//(this.orderlines).forEach((el) => sum += (((el.price*el.quantity)*(100-el.discount))/100));
//console.log(sum);


    }
});