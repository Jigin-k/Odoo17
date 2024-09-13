/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
export function chunk(array, size) {
    console.log(array)
    console.log(array.length, "hell")
    var result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
    }


PublicWidget.registry.subscription_credits_snippet = PublicWidget.Widget.extend({
    selector: '.credit_dynamic_snippet',

    willStart: async function () {
        const data = await jsonrpc('/subscription_credits_snippet', {});
        console.log(data);
        this.sub_credits = data;
    },

    start: function () {
        const uniqueId = `credit-carousel-${Math.floor(Math.random() * 1000)}`;
        console.log(uniqueId)
        const chunks = chunk(this.sub_credits,4)
        chunks[0].is_active = true
        var refEl = this.$el.find("#subscription_credits_carousel");

        refEl.html(renderToElement('recurring_subscription.subscription_credit_snippet_template', {
            chunks,
            uniqueId
        }));
    }
});
