import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { CalculatorPopup } from "@pos_calculator/js/calculator_popup";

patch(ControlButtons.prototype,{
    async onclickCalculator() {
          await makeAwaitable(this.dialog, CalculatorPopup, {
            title: _t("Calculator"),
        });
//        const { confirmed, payload } = await makeAwaitable({
//            component: CalculatorPopup,
//            props: {
//                title: _t("Simple Calculator"),
//                startingValue: "0",
//            },
//        });

    },
});
