/** @odoo-module */

import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            product_brand: this.get_product().product_brand[1],

        };
    },
});
