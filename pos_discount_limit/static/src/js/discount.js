/** @odoo-module */


import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


patch(Order.prototype, {
   async pay() {
   console.log(this)
   if (this.pos.config.amount_discount_limit && this.get_total_discount()){
    var TotalSessionDiscount = await this.env.services.orm.call('pos.order','total_session_discount',[this.pos_session_id])
    var DiscountLimit = this.pos.config.amount_discount_limit
    var CurrentOrderDiscount = this.get_total_discount()

    console.log(TotalSessionDiscount)
    console.log(DiscountLimit)
    console.log(CurrentOrderDiscount)

    if ((CurrentOrderDiscount > DiscountLimit) || ((TotalSessionDiscount + CurrentOrderDiscount) > DiscountLimit)){
        this.env.services.popup.add(ErrorPopup, {
            title:"Payment Cannot be Processed",
            body:"Discount Limit For Current Session Has Been Reached",
        });
    }
    else {
       return {
           ...super.pay(...arguments)
       };
       }
   }
   else {
       return {
           ...super.pay(...arguments)
       };
       }
}
});