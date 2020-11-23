odoo.define('flag_barcode.tree_header_extend', function (require){
    "use strict";
    var core = require('web.core');
    var ListView = require('web.ListView');
    var ListController = require("web.ListController");
    var rpc = require('web.rpc');

    var includeDict = {
        renderButtons: function () {
            console.log('Test@moha');
            this._super.apply(this, arguments);
            if (this.modelName == 'generate.barcode.flag') {
                var your_btn = this.$buttons.find('button.create_selected_prods');
                your_btn.on('click', this.proxy('create_selected_prods'));
            }
        },
        create_selected_prods: function(){

//        TO OPEN A WIZARD
         this.do_action({
                name: "Open a wizard",
                type: 'ir.actions.act_window',
                res_model: 'so.select.products.demo',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
            });

//        THIS IF U WANT TO EXECUTE A FUNCTION
//            return this._rpc({
//                        model: 'generate.barcode.flag',
//                        method: 'addproduct_action',
//                        args: [self.given_context],
//                    })

        }
    };

    ListController.include(includeDict);
});