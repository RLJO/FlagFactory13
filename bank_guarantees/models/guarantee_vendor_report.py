from odoo import models, fields, api


class GuaranteeVendorReportWizard(models.TransientModel):
    _name = 'guarantee.vendor.report.wizard'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", default=fields.Date.today)

    state = fields.Selection([('draft','Draft'),
                              ('approved','Approved'),
                              ('paid','Paid'),
                              ('renew','Renew'),
                              ('end','End'),
                              ('refund','Refund')], default='draft')


    def get_guarantee_vendor_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'state': self.state,
            },
        }
        return self.env.ref('bank_guarantees.guarantee_vendor_report_report').report_action(self, data=data)


class GuaranteeVendorReportReportView(models.AbstractModel):
    _name = "report.bank_guarantees.guarantee_vendor_report_report_view"
    _description = "Guarantee Vendor Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = []
        if data['form']['start_date']:
            vendors = self.env['bank.vendor.guarantees'].search([('state', '=', data['form']['state']),
                                                        ('issue_date', '>=', data['form']['start_date']),
                                                        ('issue_date', '<=', data['form']['end_date'])
                                                        ], order='name asc')

        if data['form']['state']:
            vendors = self.env['bank.vendor.guarantees'].search([('state', '=', data['form']['state'])
                                                        ], order='name asc')

        for vendor in vendors:
            guarantee_type = dict(vendor._fields['guarantee_type'].selection).get(vendor.guarantee_type)
            state = dict(vendor._fields['state'].selection).get(vendor.state)
            docs.append({
                'start_date': data['form']['start_date'],
                'end_date': data['form']['end_date'],
                'description': vendor.description,
                'bank_name': vendor.bank_name.name,
                'vendor_id': vendor.vendor_id.name,
                'guarantee_type': guarantee_type,
                'state': state,
                'guarantee_expense': vendor.guarantee_expense,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': data['form']['start_date'],
            'date_end': data['form']['end_date'],
            'state': data['form']['state'],
            'docs': docs,
        }
