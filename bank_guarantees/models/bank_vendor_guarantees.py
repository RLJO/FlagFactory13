# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError

class BankVendorGuarantees(models.Model):
    _name = 'bank.vendor.guarantees'
    _description = 'Bank Vendor Guarandtees'
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char(string='Guarantees Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    state = fields.Selection([('draft','Draft'),
                              ('approved','Approved'),
                              ('paid','Paid'),
                              ('renew','Renew'),
                              ('end','End'),
                              ('repaid','Repaid')], default='draft')

    description = fields.Char(string="Description")
    vendor_id = fields.Many2one('res.partner', string="Vendor") #03 #domain for Vendors or verndors


    issue_date = fields.Date(string="Issue Date", required=True)
    end_date = fields.Date(string="End Date")
    renew_date = fields.Date(string="Renew Date")

    guarantee_period = fields.Char(string="Guarantees Period")

    guarantee_type = fields.Selection([('basic_g','Basic Guarantee'),('final_g','Final Guarantee')],
                                         string="Guarantees Type")

    guarantee_amount = fields.Float(string="Guarantee Amount") #04 #currency field

    guarantee_rate = fields.Float(string="Guarantee Rate") #05 #percentage %

    guarantee_total_amount = fields.Float(string="Guarantee Total Amount") #06 #currency field
    guarantee_expense = fields.Float(string="Guarantee Expense Amount") #07 #currency field

    currency_id = fields.Many2one('res.currency')
    vat = fields.Many2one('account.tax', string="VAT", domain = [('type_tax_use', '=', 'purchase')], required=True)


    bank_name = fields.Many2one('account.journal', domain=[('type', '=', 'bank')], required=True) #domain journal type = bank
    guarantee_expense_account = fields.Many2one('account.account', required=True) #from chart of accounts
    guarantee_account = fields.Many2one('account.account', required=True) #from chart of accounts
    notes = fields.Text(string="Notes")


    #Sending Email
    @api.model
    def mail_reminder(self):
        """Sending document expiry notification to employees."""

        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        recipient_partners=[]
        groups = self.env['res.groups'].search([('name', '=', 'Flags Barcode MANAGER')])
        print(groups)
        print('asd')
        for group in groups:
            print('asd1')
            for recipient in group.users:
                if recipient.partner_id.id not in recipient_partners:
                    recipient_partners.append(recipient.partner_id.id)

        actv_id = self.sudo().activity_schedule(
            'mail.mail_activity_data_todo', date_now,
            note=_(
                '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for <a href="#" data-oe-model="%s" data-oe-id="%s">%s\'s</a> Review') % (
                     self.name, self.name, self.name,
                     self.name, self.name),
            user_id=self.vendor_id.email,
            res_id=self.id,

            summary=_("Request Approve")
        )
        print("active", actv_id)

        for i in match:
            if i.end_date:
                exp_date = fields.Date.from_string(i.end_date)
                if date_now == exp_date:
                    mail_content2 = "Hello  " + str(i.vendor_id.name) + ",<br>Your Bank Guarantees " \
                                   + str(i.name) + " is expired Today Please renew it. "

                    if len(recipient_partners):
                        i.message_post(body=mail_content2,
                                       subtype='mt_comment',
                                       subject=_('Bank Guarantees-%s Expired On %s') % (i.name, i.end_date),
                                       partner_ids=recipient_partners,
                                       message_type='comment')
        for i in match:
            if i.renew_date:
                exp_date2 = fields.Date.from_string(i.renew_date)
                if date_now == exp_date2:
                    mail_content2 = "Hello  " + str(i.vendor_id.name) + ",<br>Your Bank Guarantees " \
                                   + str(i.name) + " is expired Today Please renew it. "

                    if len(recipient_partners):
                        i.message_post(body=mail_content2,
                                       subtype='mt_comment',
                                       subject=_('Bank Guarantees-%s Expired On %s') % (i.name, i.end_date),
                                       partner_ids=recipient_partners,
                                       message_type='comment')

    #######################
    #######################
    #######################
    #######################

    #Sending Activity
    def make_activity(self):

        user_Obj = self.env['res.users'].browse(self.env.user.id)
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])

        for i in match:
            if i.end_date:
                print('test1')
                exp_date = fields.Date.from_string(i.end_date)
                if date_now == exp_date:
                    print('test2')
                    act_type_xmlid = 'mail.mail_activity_data_todo'
                    print(act_type_xmlid)
                    date_deadline = datetime.now().strftime('%Y-%m-%d')
                    summary = ('Bank Guarantees-%s Expired') % (i.name)
                    note = "Hello  " + str(i.vendor_id.name) + ",<br>Your Bank Guarantees " \
                                   + str(i.name) + " is expired Today Please renew it. "

                    if act_type_xmlid:
                        print('test3')
                        activity_type = self.sudo().env.ref(act_type_xmlid)

                    model_id = self.env['ir.model']._get(self._name).id
                    print(model_id)
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': date_deadline,
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': user_Obj.id,
                    }
                    print(create_vals)
                    self.env['mail.activity'].create(create_vals)

        for i in match:
            if i.renew_date:
                print('test1')
                exp_date = fields.Date.from_string(i.renew_date)
                if date_now == exp_date:
                    print('test2')
                    act_type_xmlid = 'mail.mail_activity_data_todo'
                    print(act_type_xmlid)
                    date_deadline = datetime.now().strftime('%Y-%m-%d')
                    summary = ('Bank Guarantees-%s Expired') % (i.name)
                    note = "Hello  " + str(i.vendor_id.name) + ",<br>Your Bank Guarantees " \
                                   + str(i.name) + " is expired Today Please renew it. "

                    if act_type_xmlid:
                        print('test3')
                        activity_type = self.sudo().env.ref(act_type_xmlid)

                    model_id = self.env['ir.model']._get(self._name).id
                    print(model_id)
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': date_deadline,
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': user_Obj.id,
                    }
                    print(create_vals)
                    self.env['mail.activity'].create(create_vals)


#########################22
#########################222
#########################2222



###############################
###############################
###############################

    @api.onchange('guarantee_amount','guarantee_rate')
    def calc_currency(self):
        self.guarantee_total_amount = self.guarantee_amount * self.guarantee_rate


    def button_confirm(self):
        return self.write({'state': 'approved'})

    def button_paid(self):
        account_id = self.env['account.move']
        print('test44')
        total_vat = self.vat.amount / 100 * round(float(self.guarantee_amount),2)
        total_vat_vat = self.vat.amount / 100 * round(float(total_vat),2)
        total_after = round(float(self.guarantee_amount),2) + round(float(total_vat),2) + round(float(total_vat_vat),2)
        print(round(total_vat, 2))
        print(round(total_vat_vat, 2))
        print(total_after)
        account_id.create({
            'date': self.issue_date,
            'journal_id': self.bank_name.id,
            'ref': str('PAID '+self.name),
            'line_ids': [
                (0,0, {
                        'account_id': self.bank_name.default_credit_account_id.id,
                        'name': str(self.bank_name.name) + " [" + str(self.vendor_id.name) + "]",
                        'credit': total_after
                      }),
                (0,0, {
                        'account_id': self.vat.invoice_repartition_line_ids.account_id.id,
                        'name': "VAT " + str(self.vat.type_tax_use).capitalize() + " " + str(self.vat.name),
                        'debit': total_vat_vat
                      }),
                (0,0, {
                        'account_id': self.guarantee_expense_account.id,
                        'tax_ids': self.vat,
                        'debit': total_vat
                }),
                (0,0, {
                        'account_id': self.guarantee_account.id,
                        'name': str(self.name) + " " + str(self.description),
                        'debit': self.guarantee_amount
                      }),
                    ]
            })

        return self.write({'state': 'paid'})

    def button_renew_end(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bank.vendor.guarantees.wizard',
            'target': 'new',
        }


    def button_repaid(self):
        account_id = self.env['account.move']
        print('test55')
        account_id.create({
            'date': self.issue_date,
            'journal_id': self.bank_name.id,
            'ref': str('REPAID ' + self.name),
            'line_ids': [
                (0, 0, {
                    'account_id': self.bank_name.default_credit_account_id.id,
                    'name': str(self.bank_name.name) + " [" + str(self.vendor_id.name) + "]",
                    'credit': self.guarantee_amount
                }),

                (0, 0, {
                    'account_id': self.guarantee_account.id,
                    'name': str(self.name) + " " + str(self.description),
                    'debit': self.guarantee_amount
                }),
            ]
        })

        return self.write({'state': 'repaid'})

    def button_set_draft(self):
        return self.write({'state': 'draft'})


    @api.model
    def create(self, vals):
        print('test')
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bank.vendor.guarantees') or _('New')
        res = super(BankVendorGuarantees, self).create(vals)
        return res

    @api.onchange('issue_date', 'end_date')
    def _computed_period(self):

        if self.issue_date and self.end_date:
            fmt = '%Y-%m-%d'
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


class BankVendorGuaranteesWizard(models.Model):
    _name = 'bank.vendor.guarantees.wizard'


    def end_state(self):
        record_id = self.env['bank.vendor.guarantees'].search([('id', '=', self.env.context.get('active_id'))])
        record_id.write({'state': 'end'})
        if not record_id.end_date:
            raise ValidationError(_("Please Enter 'End Date' Field"))

    def renew_state(self):
        record_id = self.env['bank.vendor.guarantees'].search([('id', '=', self.env.context.get('active_id'))])
        record_id.end_date = ''
        record_id.guarantee_period = ''

