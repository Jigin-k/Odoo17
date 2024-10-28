/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
    publicWidget.registry.return_order = publicWidget.Widget.extend({
        selector: '#quote_content',
        events: {
            'click #return_btn': '_onReturnBtnClick',
            'change #product': '_onProductChange',
        },
        /**
         * @override
         */
        start: function () {
            this._super.apply(this, arguments);
        },

        _onReturnBtnClick: function (ev) {
            var self = this;
            ev.preventDefault();
            self.$('#return_modal').modal('show');
        },

        _onProductChange: function (ev) {
              console.log("HAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIiiiii")
            var self = this;
            var $product = $(ev.currentTarget);
            var $submitButton = self.$('#submit');
            $submitButton.toggleClass('d-none', $product.val() === 'none');
        },
    });
