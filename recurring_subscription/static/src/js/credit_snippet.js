/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";


PublicWidget.registry.subscription_credits_snippet = PublicWidget.Widget.extend({
    selector: '.credit_dynamic_snippet',

    willStart: async function () {
        const data = await jsonrpc('/subscription_credits_snippet', {});
        console.log(data);
        this.sub_credits = data;
    },

    start: function () {
        var refEl = this.$el.find("#subscription_credits_carousel");
        console.log(refEl, "refEl");
        refEl.html(renderToElement('recurring_subscription.subscription_credit_snippet_template', {
            data: this.sub_credits
        }));
    }
});