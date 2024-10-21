/** @odoo-module */

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, xml } from "@odoo/owl";
import { CalculatorPopup } from "@pos_calculator/static/src/js/calculator_popup";



patch(ControlButtons.prototype, {
    setup() {
        this.pos = usePos();
        this.popup = useService("popup")
    },

     async CalculatorPopup() {
       await this.popup.add(CalculatorPopup, {
           title: _t("Customer Details"),
       });
   }
});