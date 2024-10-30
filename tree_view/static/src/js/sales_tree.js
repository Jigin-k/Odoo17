/** @odoo-module */

import { registry } from '@web/core/registry';

import { listView } from '@web/views/list/list_view';
import { ListController } from '@web/views/list/list_controller';

export class CrmListController extends ListController {
    setup() {
        super.setup();
        console.log("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    }
}
//CrmListController.template = "tree_view.CrmSalespersonFilter";

//export const CrmSalespersonFilter = {
//    ...listView,
//    Controller: CrmListController,
//};

registry.category('views').add('crm_salesperson_list', {
    ...listView,
    Controller: CrmListController,
});
