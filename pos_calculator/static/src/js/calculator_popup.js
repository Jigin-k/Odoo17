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
        subtitle: { type: String, optional: true },
        buttons: { type: CalculatorButtonsType, optional: true },
        startingValue: { type: [Number, String], optional: true },
        feedback: { type: Function, optional: true },
        formatDisplayedValue: { type: Function, optional: true },
        placeholder: { type: String, optional: true },
        isValid: { type: Function, optional: true },
        close: Function,
    };
    static defaultProps = {
        title: _t("Confirm?"),
        startingValue: "",
        isValid: () => true,
        formatDisplayedValue: (x) => x,
        feedback: () => false,
    };

    setup() {
        this.numberBuffer = useService("number_buffer");
        this.numberBuffer.use({
            triggerAtEnter: () => this.confirm(),
            triggerAtEscape: () => this.cancel(),
        });
        this.state = useState({
            buffer: this.props.startingValue,
        });
        useBus(this.numberBuffer, "buffer-update", ({ detail: value }) => {
            this.state.buffer = value;
        });
    }
    confirm() {
        this.props.close();
    }
}