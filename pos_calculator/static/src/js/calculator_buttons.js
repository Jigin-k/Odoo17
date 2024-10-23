import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { localization } from "@web/core/l10n/localization";

export const CalculatorButtonsType = {
    type: Array,
    element: [
        {
            type: Object,
            shape: {
                value: String,
                text: { type: String, optional: true },
                class: { type: String, optional: true },
                disabled: { type: Boolean, optional: true },
            },
        },
        Number,
        String,
    ],
};
export const DECIMAL = {
    get value() {
        return localization.decimalPoint;
    },
};
export const BACKSPACE = { value: "Backspace", text: "⌫" };
export const ZERO = { value: "0" };
export const DEFAULT_LAST_ROW = [{ value: "-", text: "+/-" }, ZERO, DECIMAL];
export const EMPTY = { value: "" };


export function getButtons(lastRow, rightColumn) {
    return [
        { value: "1" },
        { value: "2" },
        { value: "3" },
        { value: "+" },
        ...(rightColumn ? [rightColumn[0]] : []),
        { value: "4" },
        { value: "5" },
        { value: "6" },
        { value: "-" },
        ...(rightColumn ? [rightColumn[1]] : []),
        { value: "7" },
        { value: "8" },
        { value: "9" },
        { value: "*" },
        ...(rightColumn ? [rightColumn[2]] : []),
        { value: "C" },
        { value: "0" },
        { value: "=" },
        { value: "/" },
        ...lastRow,
        ...(rightColumn ? [rightColumn[3]] : []),
    ];
}


export class CalculatorNumpad extends Component {
    static template = "pos_calculator.CalculatorNumpad";
    static props = {
        class: { type: String, optional: true },
        onClick: { type: Function, optional: true },
        buttons: { type: CalculatorButtonsType, optional: true },
    };
    static defaultProps = {
        class: "numpad",
    };
    get buttons() {
        return this.props.buttons || getButtons([DECIMAL, ZERO, BACKSPACE]);
    }
    setup() {
        if (!this.props.onClick) {
            this.numberBuffer = useService("number_buffer");
            this.onClick = (buttonValue) => this.numberBuffer.sendKey(buttonValue);
        } else {
            this.onClick = this.props.onClick;
        }
    }
}
