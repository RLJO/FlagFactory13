odoo.define('uat_sales_tender.progressbar', function (require) {
"use strict";

var core = require('web.core');
var utils = require('web.utils');
var AbstractField = require('web.AbstractField');

var qweb = core.qweb;
var _t = core._t;
var _lt = core._lt;


var FieldProgressBar = AbstractField.extend({
    description: _lt("Progress Bar"),
    template: "ProgressBar",
    events: {
        'change input': 'on_change_input',
        'input input': 'on_change_input',
        'keyup input': function (e) {
            if (e.which === $.ui.keyCode.ENTER) {
                this.on_change_input(e);
            }
        },
    },
    supportedFieldTypes: ['integer', 'float'],
    init: function () {
        this._super.apply(this, arguments);

        // the progressbar needs the values and not the field name, passed in options
        if (this.recordData[this.nodeOptions.current_value]) {
            this.value = this.recordData[this.nodeOptions.current_value];
        }

        // The few next lines determine if the widget can write on the record or not
        this.editable_readonly = !!this.nodeOptions.editable_readonly;
        // "hard" readonly
        this.readonly = this.nodeOptions.readonly || !this.nodeOptions.editable;

        this.canWrite = !this.readonly && (
            this.mode === 'edit' ||
            (this.editable_readonly && this.mode === 'readonly') ||
            (this.viewType === 'kanban') // Keep behavior before commit
        );

        // Boolean to toggle if we edit the numerator (value) or the denominator (max_value)
        this.edit_max_value = !!this.nodeOptions.edit_max_value;
        this.max_value = this.recordData[this.nodeOptions.max_value] || 100;

        this.title = _t(this.attrs.title || this.nodeOptions.title) || '';

        // Ability to edit the field through the bar
        // /!\ this feature is disabled
        this.enableBarAsInput = false;
        this.edit_on_click = this.enableBarAsInput && this.mode === 'readonly' && !this.edit_max_value;

        this.write_mode = false;
    },
    _render: function () {
        console.log('TEST##############################')
        var self = this;
        this._render_value();

        if (this.canWrite) {
            if (this.edit_on_click) {
                this.$el.on('click', '.o_progress', function (e) {
                    var $target = $(e.currentTarget);
                    var numValue = Math.floor((e.pageX - $target.offset().left) / $target.outerWidth() * self.max_value);
                    self.on_update(numValue);
                    self._render_value();
                });
            } else {
                this.$el.on('click', function () {
                    if (!self.write_mode) {
                        var $input = $('<input>', {type: 'text', class: 'o_progressbar_value o_input'});
                        $input.on('blur', self.on_change_input.bind(self));
                        self.$('.o_progressbar_value').replaceWith($input);
                        self.write_mode = true;
                        self._render_value();
                    }
                });
            }
        }
        return this._super();
    },
    /**
     * Updates the widget with value
     *
     * @param {Number} value
     */
    on_update: function (value) {
        if (this.edit_max_value) {
            this.max_value = value;
            this._isValid = true;
            var changes = {};
            changes[this.nodeOptions.max_value] = this.max_value;
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: changes,
            });
        } else {
            // _setValues accepts string and will parse it
            var formattedValue = this._formatValue(value);
            this._setValue(formattedValue);
        }
    },
    on_change_input: function (e) {
        var $input = $(e.target);
        if (e.type === 'change' && !$input.is(':focus')) {
            return;
        }

        var parsedValue;
        try {
            // Cover all numbers with parseFloat
            parsedValue = field_utils.parse.float($input.val());
        } catch (error) {
            this.do_warn(_t("Wrong value entered!"), _t("Only Integer or Float Value should be valid."));
        }

        if (parsedValue !== undefined) {
            if (e.type === 'input') { // ensure what has just been typed in the input is a number
                // returns NaN if not a number
                this._render_value(parsedValue);
                if (parsedValue === 0) {
                    $input.select();
                }
            } else { // Implicit type === 'blur': we commit the value
                if (this.edit_max_value) {
                    parsedValue = parsedValue || 100;
                }

                var $div = $('<div>', {class: 'o_progressbar_value'});
                this.$('.o_progressbar_value').replaceWith($div);
                this.write_mode = false;

                this.on_update(parsedValue);
                this._render_value();
            }
        }
    },
    /**
     * Renders the value
     *
     * @private
     * @param {Number} v
     */
    _render_value: function (v) {
        console.log('TEST##############################22')
        var value = this.value;
        var max_value = this.max_value;
        if (!isNaN(v)) {
            if (this.edit_max_value) {
                max_value = v;
            } else {
                value = v;
            }
        }
        value = value || 0;
        max_value = max_value || 0;

        var widthComplete;
        if (value <= max_value) {
            widthComplete = value/max_value * 100;
        } else {
            widthComplete = 100;
        }

        this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value)
            .attr('aria-valuemin', '0')
            .attr('aria-valuemax', max_value)
            .attr('aria-valuenow', value);
        this.$('.o_progressbar_complete').css('width', widthComplete + '%');

        if (!this.write_mode) {
            if (max_value !== 100) {
                this.$('.o_progressbar_value').text(utils.human_number(value) + " / " + utils.human_number(max_value));
            } else {
                this.$('.o_progressbar_value').text(utils.human_number(value) + "%");
            }
        } else if (isNaN(v)) {
            this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
            this.$('.o_progressbar_value').focus().select();
        }
    },
    /**
     * The progress bar has more than one field/value to deal with
     * i.e. max_value
     *
     * @override
     * @private
     */
    _reset: function () {
        this._super.apply(this, arguments);
        var new_max_value = this.recordData[this.nodeOptions.max_value];
        this.max_value =  new_max_value !== undefined ? new_max_value : this.max_value;
    },
    isSet: function () {
        return true;
    },
});


});
