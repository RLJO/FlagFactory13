# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError

from odoo import api, fields, models, _, SUPERUSER_ID


class EntityFlag(models.Model):
    _name = "entity.flag"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "entity"


    barcode = fields.Char(string='Barcode', required=True, copy=False, readonly=False, index=True,
                          default=lambda self: _('New'))
    iso = fields.Char('ISO')
    entity = fields.Char('Entity')
    ratio_id = fields.Many2one('flyration.flag', string="Ratio", default=lambda self: self.env['flyration.flag'].search([('ratio_related','=','1.5')]))
    place_holder = fields.Char()

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        if vals.get('barcode', _('New')) == _('New'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('entity.flag') or _('New')
        res = super(EntityFlag, self).create(vals)
        return res

    # def name_get(self):
    #     # name get function for the model executes automatically
    #     res = []
    #     for rec in self:
    #         res.append((rec.id, '%s:%s, %s' % (rec.flyration_left, rec.flyration_right, rec.entity)))
    #     return res


