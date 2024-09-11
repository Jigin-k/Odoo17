/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.CreditSnippet = publicWidget.Widget.extend({
   selector: '.dynamic_snippet',
   start: function () {
       var self = this;
       var data = jsonrpc('/subscription_credit_snippet', {}).then((data) => {
           self.$target.empty().append(data)
       });
   }
});

export default publicWidget.registry.DynamicSnippet;