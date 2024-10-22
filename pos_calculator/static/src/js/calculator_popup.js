import { _t } from "@web/core/l10n/translation";
import { useBus, useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { Numpad, buttonsType } from "@point_of_sale/app/generic_components/numpad/numpad";

export class CalculatorPopup extends Component {
    static template = "pos_calculator.CalculatorPopup";
    static components = { Numpad,Dialog };
    static props = {
        title: { type: String, optional: true },
        subtitle: { type: String, optional: true },
        startingValue: { type: String, optional: true },
        close: Function,
        getPayload: Function
    };
    static defaultProps = {
        title: _t("Calculator"),
        startingValue: "0",
    };

    setup() {
        this.state = useState({
            value: this.props.startingValue,
        });

        // Bind methods to maintain context
        this.append = this.append.bind(this);
        this.calculate = this.calculate.bind(this);
        this.clear = this.clear.bind(this);
        this.closePopup = this.closePopup.bind(this);
    }

    append(value) {
    console.log(this.state.value)
        if (this.state.value === "0") {
            this.state.value = value;
        } else {
            this.state.value += value;
        }
        console.log(this.state.value)
    }

    calculate() {
        try {
            this.state.value = eval(this.state.value).toString();
        } catch (error) {
            this.state.value = "Error";
        }
    }

    clear() {
        this.state.value = "0";
    }

    closePopup() {
        this.props.close();
    }
}
