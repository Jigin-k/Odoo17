import { _t } from "@web/core/l10n/translation";
import { useBus, useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CalculatorNumpad,CalculatorButtonsType } from "@pos_calculator/js/calculator_buttons";

export class CalculatorPopup extends Component{
    static template = "pos_calculator.Calculator_popup";
    static components = { CalculatorNumpad, Dialog };
    static props = {
        title: { type: String, optional: true },
        buttons: { type: CalculatorButtonsType, optional: true },
        startingValue: { type: [Number, String], optional: true },
        placeholder: { type: String, optional: true },
        close: Function,
    };
    static defaultProps = {
        startingValue: "",

    };

    confirm() {
        this.props.close();
    }
}