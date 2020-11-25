# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

class BankCustomerGuarantees(models.Model):
    _name = 'bank.customer.guarantees'
    _description = 'Bank Customer Guarandtees'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Guarantees Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    state = fields.Selection([('draft','Draft'),
                              ('approved','Approved'),
                              ('paid','Paid'),
                              ('renew','Renew'),
                              ('end','End'),
                              ('repaid','Repaid')], default='draft')

    description = fields.Char(string="Description", readonly=True)
    customer_id = fields.Many2one('res.partner', string="Customer") #03 #domain for customers or verndors


    issue_date = fields.Date(string="Issue Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    renew_date = fields.Date(string="Renew Date")

    guarantee_period = fields.Char(string="Guarantees Period", readonly=True)

    guarantee_type = fields.Selection([('basic_g','Basic Guarantee'),('final_g','Final Guarantee')],
                                         string="Guarantees Type")

    guarantee_amount = fields.Float(string="Guarantee Amount") #04 #currency field
    guarantee_rate = fields.Float(string="Guarantee Rate") #05 #percentage %

    guarantee_total_amount = fields.Float(string="Guarantee Total Amount") #06 #currency field
    guarantee_expense = fields.Float(string="Guarantee Expense Amount") #07 #currency field

    currency_id = fields.Many2one('res.currency', required=True)
    vat = fields.Many2one('account.tax', string="VAT", domain = [('type_tax_use', '=', 'sale')], required=True)


    bank_name = fields.Many2one('account.journal', domain=[('type', '=', 'bank')], required=True) #domain journal type = bank
    guarantee_expense_account = fields.Many2one('account.account', required=True) #from chart of accounts
    guarantee_account = fields.Many2one('account.account', required=True) #from chart of accounts
    notes = fields.Text(string="Notes")


    @api.onchange('guarantee_amount','guarantee_rate')
    def calc_currency(self):
        self.guarantee_total_amount = self.guarantee_amount * self.guarantee_rate

    def button_confirm(self):
        return self.write({'state': 'approved'})

    def button_paid(self):

        return self.write({'state': 'paid'})

    def button_renew_end(self):
        return self.write({'state': 'end'})

    def button_repaid(self):
        return self.write({'state': 'repaid'})

    def button_set_draft(self):
        return self.write({'state': 'draft'})


    @api.model
    def create(self, vals):
        print('test')
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bank.customer.guarantees') or _('New')
        res = super(BankCustomerGuarantees, self).create(vals)
        return res

    @api.onchange('issue_date', 'end_date')
    def _computed_period(self):
        fmt = '%Y-%m-%d'
        if self.issue_date and self.end_date:
            frst_date = str(self.issue_date)
            scnd_date = str(self.end_date)
            d1 = datetime.strptime(frst_date, fmt)
            d2 = datetime.strptime(scnd_date, fmt)
            total_period = (d2 - d1).days
            if total_period > 1 or total_period == 0:
                total_period = str(total_period) + str(" Days")
                self.guarantee_period = total_period
            elif total_period == 1:
                total_period = str(total_period) + str(" Day")
                self.guarantee_period = total_period
