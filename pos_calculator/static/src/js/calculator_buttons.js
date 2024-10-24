// calculator.js
import { useService } from "@web/core/utils/hooks";
import { localization } from "@web/core/l10n/localization";
import { useState, Component } from "@odoo/owl";

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

export function getButtons() {
    return [
        { value: "1", style: 'background: silver;  border-radius: 50%;' },
        { value: "2", style: 'background: silver; border-radius: 50%;' },
        { value: "3", style: 'background: silver; border-radius: 50%;' },
        { value: "+", style: 'background: silver;' },
        { value: "4", style: 'background: silver; border-radius: 50%;' },
        { value: "5", style: 'background: silver; border-radius: 50%;' },
        { value: "6", style: 'background: silver; border-radius: 50%;' },
        { value: "-", style: 'background: silver;' },
        { value: "7", style: 'background: silver; border-radius: 50%;' },
        { value: "8", style: 'background: silver; border-radius: 50%;' },
        { value: "9", style: 'background: silver; border-radius: 50%;' },
        { value: "*", style: 'background: silver;' },
        { value: "AC", style: 'background: red  ; '   },
        { value: "0", style: 'background: silver; border-radius: 50%;' },
        { value: "=", style: 'background: silver;' },
        { value: "/", style: 'background: silver;' },
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
        startingValue: "",
    };

    setup() {
        this.numberBuffer = useService("number_buffer");
        
        this.state = useState({
            buffer: this.props.startingValue,
        });
        this.result = null;
        
        if (!this.props.onClick) {
            this.onClick = (buttonValue) => this.handleButtonClick(buttonValue);
        } else {
            this.onClick = this.props.onClick;
        }
    }

    handleInput(ev) {
        const validInput = ev.target.value.replace(/[^0-9+\-*/.]/g, '');
        this.state.buffer = validInput;
    }

    handleKeyDown(ev) {
        if (ev.key === 'Enter') {
            ev.preventDefault();
            this.calculateResult();
        } else if (ev.key === 'Escape') {
            ev.preventDefault();
            this.clear();
        } else if (ev.key === 'Backspace') {
            return true;
        }
    }

    handleButtonClick(buttonValue) {
        if (buttonValue === "=") {
            this.calculateResult();
        } else if (buttonValue === "AC") {
            this.clear();
        } else {
            this.state.buffer += buttonValue;
        }
    }

    calculateResult() {
            this.result = eval(this.state.buffer);
            this.state.buffer = this.result.toString();
    }

    clear() {
        this.state.buffer = '';
    }

    get buttons() {
        return getButtons([DECIMAL, ZERO, BACKSPACE]);
    }
}