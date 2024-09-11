/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
console.log("loading", publicWidget);

publicWidget.registry.orderDate = publicWidget.Widget.extend({
    selector: '.subscription_order_rows',
    events: {
        'change #order_date': '_onOrderDateChange'
    },

    _onOrderDateChange: function (ev) {
        console.log("hi111111111111111");

        var orderDate = $(ev.currentTarget).val();
        console.log(orderDate);

        var orderDateObj = new Date(orderDate);

        var dueDate = new Date(orderDateObj);
        dueDate.setDate(dueDate.getDate() + 15);

        var nextBillingDate = new Date(orderDateObj);
        nextBillingDate.setMonth(nextBillingDate.getMonth() + 1);

        console.log(dueDate);
        console.log(nextBillingDate);

        var formatDate = function(date) {
            var day = ('0' + date.getDate()).slice(-2);
            var month = ('0' + (date.getMonth() + 1)).slice(-2);
            var year = date.getFullYear();
            return year + '-' + month + '-' + day;
        };

        this.$('#due_date').val(formatDate(dueDate));
        this.$('#next_billing').val(formatDate(nextBillingDate));
    }
});