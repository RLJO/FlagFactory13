# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from .calverter import Calverter


class HREmployeeInherit(models.Model):
    _inherit = 'hr.employee'


    # protection
    def document_view_protection(self):
        self.ensure_one()
        domain = [
            ('emp_id', '=', self.id)]

        return {
            'name': _('Protections'),
            'domain': domain,
            'res_model': 'hr.protection',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click To Create For New Records
                        </p>'''),
            'limit': 80,
            'context': "{'default_emp_id': %s}" % self.id,
        }

    def _document_count_protection(self):
        for each in self:
            document_ids2 = self.env['hr.protection'].sudo().search([('emp_id', '=', each.id)])
            each.document_count_protection = len(document_ids2)
            # print(document_ids2.emp_id.name)
            # print(self.name)

    document_count_protection = fields.Integer(compute='_document_count_protection', string='# Protections')



    @api.model
    def _get_lang(self):
        return self.env['res.lang'].get_installed()

    emp_lang = fields.Selection(selection='_get_lang', string='Language')
    emp_exp = fields.Char(_('Experience'))
    emp_date_start = fields.Date(_('Work Starting Date'))
    emp_insurance_num = fields.Char(_('Medical insurance number'))
    emp_job_data = fields.Char(_('Job Data'))


    birthday_hijri = fields.Char(string='Date of Birth Hajri',compute='_calculate_birthday_hajri')

    @api.depends('birthday')
    def _calculate_birthday_hajri(self):
        cal = Calverter()
        if self.birthday:
            d = self.birthday
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.birthday_hijri = str(hj[2]) + "/" + str(hj[1])+ "/" + str(hj[0])
        else:
            self.birthday_hijri =""

class HRContractInherit(models.Model):
    _inherit = 'hr.contract'


    date_start_hijri = fields.Char(string='Start Date Hajri',compute='_calculate_start_date_hajri')
    date_end_hijri = fields.Char(string='End Date Hajri',compute='_calculate_date_end_hajri')
    trial_date_end_hijri = fields.Char(string='Trial Date End Hajri',compute='_calculate_trial_date_end_hajri')

    @api.depends('date_start')
    def _calculate_start_date_hajri(self):
        cal = Calverter()
        if self.date_start:
            d = self.date_start
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.date_start_hijri = str(hj[2]) + "/" + str(hj[1])+ "/" + str(hj[0])
        else:
            self.date_start_hijri =""

    @api.depends('date_end')
    def _calculate_date_end_hajri(self):
        cal = Calverter()
        if self.date_end:
            d = self.date_end
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.date_end_hijri = str(hj[2]) + "/" + str(hj[1])+ "/" + str(hj[0])
        else:
            self.date_end_hijri =""

    @api.depends('trial_date_end')
    def _calculate_trial_date_end_hajri(self):
        cal = Calverter()
        if self.trial_date_end:
            d = self.trial_date_end
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.trial_date_end_hijri = str(hj[2]) + "/" + str(hj[1])+ "/" + str(hj[0])
        else:
            self.trial_date_end_hijri =""