import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useRef, onMounted } from "@odoo/owl";

export class CalculatorPopup extends Component {
    static template = "pos_calculator.CalculatorPopup";
    static props = {
        title: String,
        confirm: Function,
        close: Function,
    };

    confirm() {
        this.props.close();
        this.props.confirm();
    }
}