# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError

from datetime import datetime, timedelta, date

from .calverter import Calverter
from odoo import api, fields, models, _, SUPERUSER_ID
# from odoo.osv import expression
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
# from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES


_STATES = [
    ('draft', 'Draft'),
    ('approve', 'Approved'),
    ('print', 'Printed'),
    ('confirm', 'Confirmed'),
    ('cancel', 'Canceled'),
]

class SalesTender(models.Model):
    _name = "sales.tender"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Tender Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    # Department = fields.Many2one()
    tender_ids = fields.One2many("sales.tender.lines", "tender_id")
    tender_no = fields.Char("Tender Number")
    created_so = fields.Many2one('sale.order', "Sale Order", readonly=True)

    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')

    # samples_att = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id', string="Samples Attachment")
    # contract_att = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id', string="Contract Attachment")

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string="Partner", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    ordering_date = fields.Date(string="Ordering Date", tracking=True, required=True)
    ordering_date_hijri = fields.Char(string="Ordering Hijri Date", compute="_calculate_hajri")
    deadline_date = fields.Date(string='Deadline Date', tracking=True, required=True)
    deadline_date_hijri = fields.Char(string='Deadline Hijri Date', compute="_calculate_hajri")


    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    c_state = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country = fields.Many2one('res.country', string='Country', ondelete='restrict')
    website = fields.Char()

    status_tender = fields.Char("Status", store=True)

    place_holder = fields.Char()
    displayed_remained_days = fields.Char("Days Left", compute="date_progress1", store=True)
    remained_days = fields.Float("Days Remind", compute="date_progress1", default=-.5)
    # date_today = fields.Date(default=fields.Date.today())

    date_progress = fields.Integer(compute="date_progress1", string='Days Left Percentage', store=True, recompute=True)

    @api.onchange('country')
    def compute_qty_delivered(self):
        for record in self.tender_ids:
            for rec in self.created_so.order_line:
                if rec.product_id == record.product_id:
                    record.qty_delivered = rec.qty_delivered

        x_qty = sum(x.quantity for x in self.tender_ids)
        y_qty_delivered = sum(x.qty_delivered for x in self.tender_ids)
        if x_qty > 0:
            if x_qty == y_qty_delivered:
                self.status_tender = "Done Delivered"
            else:
                self.status_tender = "Not Delivered"




    @api.depends('deadline_date', 'ordering_date')
    def date_progress1(self):
        print("TEST")
        fmt = '%Y-%m-%d'
        if self.deadline_date and self.ordering_date:
            frstdate = str(date.today())
            scnddate = str(self.deadline_date)
            d1 = datetime.strptime(frstdate, fmt)
            d2 = datetime.strptime(scnddate, fmt)

            self.remained_days = (d2 - d1).days

        if self.ordering_date and self.deadline_date:
            frst_date = str(self.ordering_date)
            scnd_date = str(self.deadline_date)
            d1 = datetime.strptime(frst_date, fmt)
            d2 = datetime.strptime(scnd_date, fmt)
            total1 = (d2 - d1).days

            thrd_date = str(self.ordering_date)
            frth_date = str(date.today())
            d3 = datetime.strptime(thrd_date, fmt)
            d4 = datetime.strptime(frth_date, fmt)
            total2 = (d4 - d3).days
            if total1 > 0:
                calc = (total2/total1)
            print(calc)

        x = self.remained_days

        if self.deadline_date and self.ordering_date:
            if x <= -1: #To dont let the percentage increase than 100% if date expired
                calc = 1
                self.date_progress = (calc * 100) / 1
            print(self.date_progress)

        if self.deadline_date and self.ordering_date:
            if x > 1:
                self.displayed_remained_days = str(x) + str(" Days")
            elif x == 1:
                self.displayed_remained_days = str(x) + str(" Day")
            elif x == 0 or x <= -1:
                if self.status_tender == "Not Delivered":
                    self.displayed_remained_days = "Expired"
                elif self.status_tender == "Done Delivered":
                    self.displayed_remained_days = "Done"



    @api.depends('ordering_date','deadline_date')
    def _calculate_hajri(self):
        cal = Calverter()

        if self.ordering_date:
            d = self.ordering_date
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.ordering_date_hijri = str( hj[2])+ "/"+ str(hj[1])+ "/"+str(hj[0])
        else:
            self.ordering_date_hijri = ""

        if self.deadline_date:
            d = self.deadline_date
            jd = cal.gregorian_to_jd(d.year, d.month, d.day)
            hj = cal.jd_to_islamic(jd)
            self.deadline_date_hijri =str( hj[2])+ "/"+ str(hj[1])+ "/"+str(hj[0])
        else:
            self.deadline_date_hijri =""



    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.tender') or _('New')
        res = super(SalesTender, self).create(vals)
        return res


    def create_tender_so(self):
        self.button_confirm()
        tender_id = self.env['sale.order']

        tender_obj = tender_id.create({
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'created_tender': self.id,
            'order_line': [
                (0, 0, {
                    'product_id': tender.product_id.id,
                    'product_uom_qty': tender.quantity,
                    'qty_delivered': tender.qty_delivered,
                    'price_unit': tender.price,
                }) for tender in self.tender_ids]
        })
        self.created_so = tender_obj
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Tender',
            'res_model': 'sale.order',
            'res_id': tender_obj.id,
            'view_mode': 'form',
            'target': 'current',
        }


    def print_report_action(self):
        return self.env.ref('uat_sales_tender.sales_tender_report_id').report_action(self)

    def button_approve(self):
        return self.write({'state': 'approve'})

    def button_confirm(self):
        return self.write({'state': 'confirm'})

    def button_cancel(self):
        return self.write({'state': 'cancel'})

    def button_to_draft(self):
        return self.write({'state': 'draft'})


    def _document_count(self):
        for each in self:
            document_ids = self.env['tender.document'].sudo().search([('tender_ref', '=', each.id)])
            each.document_count = len(document_ids)

    def document_view(self):
        self.ensure_one()
        domain = [
            ('tender_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'tender.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_tender_ref': '%s'}" % self.id
        }

    document_count = fields.Integer(compute='_document_count', string='# Documents')



class TenderSaleOrder(models.Model):
    _inherit = "sale.order"

    created_tender = fields.Many2one('sales.tender', "Tender", readonly=True, required=False)



class SalesTenderLines(models.Model):
    _name = "sales.tender.lines"

    tender_id = fields.Many2one("sales.tender")

    so_line = fields.Many2one("sale.order")
    product_id = fields.Many2one("product.product", "Items Requested")
    description = fields.Text(string="Description", readonly=False)
    product_uom_id = fields.Many2one('uom.uom', related='product_id.uom_id', readonly=True, String='UnitMeasure')
    quantity = fields.Float(string="Quantity")
    qty_delivered = fields.Float(string="Qty Delivered", readonly=True)
    # delivered_status = fields.Char("Status")

    price = fields.Float(string="Price")
    standard_price = fields.Float(string="Cost")
    note = fields.Char()
    total = fields.Float(compute="compute_total_price")
    sequence = fields.Integer()
    # purchase_boolean = fields.Boolean(string="Purchase", default=False)
    purch_or_prod = fields.Selection([('prod','Production'),('purch','Purchase')])

    @api.depends('quantity', 'price')
    def compute_total_price(self):
        for record in self:
            record.total = record.quantity * record.price


    def _document_count2(self):
        for each in self:
            document_idss = self.env['product.tender.document'].sudo().search([('product_ref', '=', each.id)])
            each.document_count2 = len(document_idss)

    def document_view2(self):
        self.ensure_one()
        domain = [
            ('product_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'product.tender.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_product_ref': '%s'}" % self.id
        }

    document_count2 = fields.Integer(compute='_document_count2', string='# Documents')
