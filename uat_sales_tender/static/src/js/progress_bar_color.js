odoo.define('progress_bar_color.ProgressBar', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var Widget = require('web.Widget');
var ProgressBar = require('web.ProgressBar')
var Model = require('web.DataModel');

var QWeb = core.qweb;
var _t = core._t;


ProgressBar.include({

    _render_value: function(v) {
        alert('TESTING ... WORKING??222');
        console.log('TESTING ... WORKING??333');

        var value = this.value;
        var max_value = this.max_value;
        if(!isNaN(v)) {
            if(this.edit_max_value) {
                max_value = v;
            } else {
                value = v;
            }
        }
        value = value || 0;
        max_value = max_value || 0;

        var widthComplete;
        if(value <= max_value) {
            widthComplete = value/max_value * 100;
        } else {
            widthComplete = max_value/value * 100;
        }
        this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
        this.$('.o_progressbar_complete').toggleClass('o_progress_gt_fty', widthComplete > 50).css('width', widthComplete + '%');
        this.$('.o_progressbar_complete').toggleClass('o_progress_lt_fty', widthComplete <= 50).css('width', widthComplete + '%');

        if(this.readonly) {
            if(max_value !== 100) {
                this.$('.o_progressbar_value').html(utils.human_number(value) + " / " + utils.human_number(max_value));
            } else {
                this.$('.o_progressbar_value').html(utils.human_number(value) + "%");
            }
        } else if(isNaN(v)) {
            this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
        }
    },

    });


});