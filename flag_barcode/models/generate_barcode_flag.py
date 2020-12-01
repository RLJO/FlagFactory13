# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError


class GenerateBarcodeFlag(models.Model):
    _name = "generate.barcode.flag"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "barcode"
    _order = "id desc"

    generate_code_lines = fields.Many2many('generate.barcode.flag.line', 'generate_code')

    barcode = fields.Char('Flag Barcode', readonly=True)

    category_id = fields.Many2one('flag.category', 'Category')
    flyration_id = fields.Many2one('flyration.flag', "Ratio")
    nomenclature_id = fields.Many2one('nomenclature.flag', 'Nomenclature')
    height_nomenclature = fields.Float("Height", store=True, compute="_get_height")
    width_nomenclature = fields.Float("Width", store=True, compute="_get_height")
    entity_id = fields.Many2one('entity.flag', 'Entity')
    material_id = fields.Many2one('material.flag', 'Material')
    material_color_id = fields.Many2one('material.color.flag', 'Material Color')
    image_id = fields.Many2one('image.flag', 'Image')
    faces_id = fields.Many2one('faces.flag', 'Face')
    affixment_id = fields.Many2one('affixment.flag', 'Affixment')
    image = fields.Binary("Image")
    description = fields.Text("Description")
    product_id = fields.Many2one('generate.barcode.flag.line', 'generated Product' , readonly=True)



    product_name = fields.Char("Product Name")

    product_type = fields.Selection([('consu','Consumable'),
                                     ('service','Service'),
                                     ('product','Storable Product')], default='product')
    product_category = fields.Many2one('product.category', "Product Category", default= lambda self: self.env['product.category'].search([('name', '=', 'All')]))
    created_product = fields.Many2one('product.product','Generated Product', readonly=True)
    current_user = fields.Many2one('res.users')

    # generate.barcode.flag
    prod_check = fields.Boolean(default=False)
    color_selected = fields.Boolean(default=False)


    test_prod = fields.Many2one('select.products.demo')


    def addproduct_action(self):

        self.active_id = True
        self.color_selected = True
        prod_exist = self.env['select.products.demo'].search([('created_product', '=', self.created_product.id)])
        if not prod_exist:
            self.env['select.products.demo'].create({
                'created_product': self.created_product.id,
                'current_user': self.current_user.env.user.id,
            })
        print(prod_exist)

        # for i in x_prods:
        #     self.product_list.append(i)
        # self.product_list_all.append(self.product_list)
        # print(self.product_list)
        # print('####################################################')
        # print(self.product_list_all)
        #
        # self.product_list.clear()

    # def create_all_prods(self):
    #     print(self.product_list)
    #     for prods_all in self.product_list_all:
    #         for prods in prods_all:
    #             print(prods[0])
    #             print(prods[1])
    #             self.env['select.products'].sudo().create({
    #                 'created_product': prods[0],
    #                 'current_user': prods[1],
    #             })

    # def create_all_prods(self):
    #     print(self.product_list)
    #     for prods_all in self.product_list_all:
    #         for prods in prods_all:
    #             self.env['product.template'].sudo().create({
    #                 'barcode': prods[0],
    #                 'default_code': prods[0],
    #                 'name': prods[1],
    #                 'type': prods[2],
    #                 'categ_id': prods[3],
    #                 'image_1920': prods[4],
    #                 'description': prods[5],
    #                 'flyration_id': prods[6],
    #                 'category_id': prods[7],
    #                 'nomenclature_id': prods[8],
    #                 'height_nomenclature': prods[9],
    #                 'width_nomenclature': prods[10],
    #                 'entity_id': prods[11],
    #                 'material_id': prods[12],
    #                 'material_color_id': prods[13],
    #                 'image_id': prods[14],
    #                 'faces_id': prods[15],
    #                 'affixment_id': prods[16],
    #                 'generate_code': prods.id,
    #
    #             })


    #     # return {
    #     #     'type': 'ir.actions.act_window',
    #     #     'name': 'Product Template',
    #     #     'res_model': 'product.template',
    #     #     'res_id': rec_id.id,
    #     #     'view_mode': 'form',
    #     #     'target': 'current',
    #     # }




    @api.onchange('nomenclature_id','material_color_id','material_id','image_id','faces_id','affixment_id')
    def change_prod(self):
        print('itest')
        x = ('[%s] %s x %s %s %s %s %s' % (self.nomenclature_id.nomenclature,self.height_nomenclature\
                                             ,self.width_nomenclature,self.material_color_id.color\
                                             ,self.material_id.material_type,self.image_id.image\
                                             ,self.faces_id.faces))
        y = x.replace("False", '')
        self.product_name = y

    def create_prod(self):
        barcode_rec = self.env['product.product'].search([('barcode', '=', self.barcode)])
        rec_id = self.env['product.product'].sudo().create({
            'barcode': self.barcode,
            'default_code': self.barcode,
            'name': self.product_name,
            'type': self.product_type,
            'categ_id': self.product_category.id,
            'image_1920': self.image,
            'description': self.description,
            'flyration_id': self.flyration_id.ratio_related,
            'category_id': self.category_id.category,
            'nomenclature_id': self.nomenclature_id.nomenclature,
            'height_nomenclature': self.height_nomenclature,
            'width_nomenclature': self.width_nomenclature,
            'entity_id': self.entity_id.entity,
            'material_id': self.material_id.material_type,
            'material_color_id': self.material_color_id.color,
            'image_id': self.image_id.image,
            'faces_id': self.faces_id.faces,
            'affixment_id': self.affixment_id.affixment,
            'generate_code': self.id,

        })
        self.prod_check = True
        self.created_product = rec_id
        print(rec_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Template',
            'res_model': 'product.product',
            'res_id': rec_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def update_prod(self):
        barcode_rec = self.env['product.product'].search([('barcode', '=', self.barcode)])
        barcode_rec.sudo().update({
            'barcode': self.barcode,
            'default_code': self.barcode,
            'name': self.product_name,
            'type': self.product_type,
            'categ_id': self.product_category.id,
            'image_1920': self.image,
            'description': self.description,
            'flyration_id': self.flyration_id.ratio_related,
            'category_id': self.category_id.category,
            'nomenclature_id': self.nomenclature_id.nomenclature,
            'height_nomenclature': self.height_nomenclature,
            'width_nomenclature': self.width_nomenclature,
            'entity_id': self.entity_id.entity,
            'material_id': self.material_id.material_type,
            'material_color_id': self.material_color_id.color,
            'image_id': self.image_id.image,
            'faces_id': self.faces_id.faces,
            'affixment_id': self.affixment_id.affixment,
            'generate_code': self.id,

        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Template',
            'res_model': 'product.product',
            'res_id': barcode_rec.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def create_variant(self):
        barcode_rec = self.env['product.product'].search([('barcode', '=', self.barcode)])
        barcode_rec.sudo().create({
            'attribute_line_ids': [[0, 0, {
                            'attribute_id': 'Height',
                            'value_ids': [
                                [0, 0, {'name': 'red', 'attribute_id': 17, 'sequence': 1}],
                                [0, 0, {'name': 'blue', 'attribute_id': 19, 'sequence': 2}],
                            ],
                        }]]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Template',
            'res_model': 'product.product',
            'res_id': barcode_rec.id,
            'view_mode': 'form',
            'target': 'current',
        }
        self.created_product = rec_id



    @api.onchange("entity_id", "nomenclature_id")
    def entity_func(self):
        self.flyration_id = self.entity_id.ratio_id
        self.nomenclature_id.ration = self.entity_id.ratio_id.ratio_related
        return 0

    # @api.onchange("entity_id", "nomenclature_id", "height_nomenclature")
    # def _calc_width(self):
    #     # if self.nomenclature_id.nomenclature == "Diplomat Car Flag":
    #     #     print("111")
    #     #     self.width_nomenclature = 30
    #     #     if self.nomenclature_id.ration != 0:
    #     #         self.height_nomenclature = self.width_nomenclature/self.nomenclature_id.ration
    #     #     print("SUCCESS")
    #     #
    #     # if self.nomenclature_id.nomenclature != "Diplomat Car Flag":
    #     # for rec in self:
    #     #     if rec.height_nomenclature  and rec.nomenclature_id.ration:
    #     #         rec.width_nomenclature = rec.height_nomenclature * rec.nomenclature_id.ration

    @api.depends("entity_id", "nomenclature_id","height_nomenclature")
    def _get_height(self):
        if self.nomenclature_id.nomenclature == "Desk Top Flag" and self.nomenclature_id.ration > 1.5:
            print("111")
            self.height_nomenclature = self.nomenclature_id.height
            if self.nomenclature_id.ration != 0:
                new_rasio = 1.5/self.nomenclature_id.ration
                self.height_nomenclature = self.nomenclature_id.height * new_rasio

        elif self.nomenclature_id.nomenclature == "Diplomat Car Flag" and self.nomenclature_id.ration > 1.5:
             print("222")
             self.width_nomenclature = 30
             if self.nomenclature_id.ration != 0:
                self.height_nomenclature = self.width_nomenclature/self.nomenclature_id.ration
                print("SUCCESS")
        else:
            print("333")
            self.height_nomenclature = self.nomenclature_id.height

        self.width_nomenclature = self.height_nomenclature * self.nomenclature_id.ration

    @api.depends("flyration_id", "nomenclature_id", "entity_id",
                 "material_id", "material_color_id", "image_id", "faces_id", "affixment_id")
    def generate_flag_barcode(self):
        #collecting fields values together to generate a barcode, disappear if false.
        barcode_x = ('%s%s%s%s%s%s%s%s%s' % (self.category_id.barcode, self.flyration_id.barcode, self.nomenclature_id.barcode,
                                         self.entity_id.barcode, self.material_id.barcode, self.material_color_id.barcode,
                                         self.image_id.barcode, self.faces_id.barcode,
                                         self.affixment_id.barcode))
        if "False" in barcode_x:
            barcode_y = barcode_x.replace("False", '')
            self.barcode = barcode_y
        else:
            self.barcode = barcode_x
        barcode_rec = self.env['generate.barcode.flag.line'].search([('barcode','=',self.barcode)])
        if barcode_rec :
            rec_id = barcode_rec.sudo().update({
                'barcode': self.barcode,
                'flyration_id': self.flyration_id.ratio_related,
                'category_id': self.category_id.category,
                'nomenclature_id': self.nomenclature_id.nomenclature,
                'entity_id': self.entity_id.entity,
                'material_id': self.material_id.material_type,
                'material_color_id': self.material_color_id.color,
                'image_id': self.image_id.image,
                'faces_id': self.faces_id.faces,
                'affixment_id': self.affixment_id.affixment,
                'generate_code': self.id,

            })
            self.product_id = rec_id
        else:
            rec_id = self.env['generate.barcode.flag.line'].sudo().create({
                                    'barcode': self.barcode,
                                    'flyration_id': self.flyration_id.ratio_related,
                                    'category_id': self.category_id.category,
                                    'nomenclature_id': "%s, %s (%s x %s)" % (self.nomenclature_id.nomenclature, self.nomenclature_id.ration, self.nomenclature_id.height, self.nomenclature_id.width),
                                    'entity_id': self.entity_id.entity,
                                    'material_id': self.material_id.material_type,
                                    'material_color_id': self.material_color_id.color,
                                    'image_id': self.image_id.image,
                                    'faces_id': self.faces_id.faces,
                                    'affixment_id': self.affixment_id.affixment,
                                    'generate_code': self.id,
                                     })
            self.product_id = rec_id
            print(rec_id)


    # def write(self, vals):
    #     res = super(GenerateBarcodeFlag, self).write(vals)
    #     self.nomenclature_id.height = self.nomenclature_id.height_stored
    #
    #     return res


    # @api.model
    # def default_get(self, fields):
    #     res = super(GenerateBarcodeFlag, self).default_get(fields)
    #     barcode_lines = []
    #     barcode_rec = self.env['generate.barcode.flag.line'].search([])
    #     for pro in barcode_rec:
    #         line = (0, 0, {
    #             'barcode': pro.barcode,
    #             'flyration_id': pro.flyration_id,
    #             'category_id': pro.category_id,
    #             'nomenclature_id': pro.nomenclature_id,
    #             'entity_id': pro.entity_id.entity,
    #             'material_id': pro.material_id,
    #             'material_color_id': pro.material_color_id,
    #             'image_id': pro.image_id,
    #             'faces_id': pro.faces_id,
    #             'affixment_id': pro.affixment_id,
    #         })
    #         barcode_lines.append(line)
    #
    #     return res


class TranslateCategoryAr(models.Model):
    _inherit = "product.category"
    name = fields.Char('Name', index=True, required=True, translate=True)


class TranslateCustomerAr(models.Model):
    _inherit = "res.partner"
    name = fields.Char('Name', translate=True)


class CustomProductTemplate(models.Model):
    _inherit = "product.product"

    category_id = fields.Char('Flyration', readonly=True)
    flyration_id = fields.Float('Flyration', readonly=True)
    nomenclature_id = fields.Char('Nomenclature', readonly=True)
    height_nomenclature = fields.Float('Height', readonly=True)
    width_nomenclature = fields.Float('Width', readonly=True)
    entity_id = fields.Char('Entity', readonly=True)
    material_id = fields.Char('Material', readonly=True)
    material_color_id = fields.Char('Material Color', readonly=True)
    image_id = fields.Char('Image', readonly=True)
    faces_id = fields.Char('Face', readonly=True)
    affixment_id = fields.Char('Affixment', readonly=True)
    generate_code = fields.Many2one('generate.barcode.flag', string="Generated Barcode")

class GenerateBarcodeFlagLines(models.Model):
    _name = "generate.barcode.flag.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "barcode"

    generate_code = fields.Many2one('generate.barcode.flag')

    barcode = fields.Char('Flag Barcode')
    category_id = fields.Char('Flyration')
    flyration_id = fields.Float('Flyration')
    nomenclature_id = fields.Char('Nomenclature')
    entity_id = fields.Char('Entity')
    material_id = fields.Char('Material')
    material_color_id = fields.Char('Material Color')
    image_id = fields.Char('Image')
    faces_id = fields.Char('Face')
    affixment_id = fields.Char('Affixment')

class SelectProductsDemo(models.Model):
    _name = 'select.products.demo'

    created_product = fields.Many2one('product.product', 'Product')
    current_user = fields.Many2one('res.users', 'Current User')

class SoSelectProductsDemo(models.Model):
    _name = 'so.select.products.demo'

    partner_id = fields.Many2one('res.partner', string="Partner")
    selected_prod_id = fields.Many2one('select.products.demo')
    generated_barcode_id = fields.Many2one('generate.barcode.flag')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)



    def create_product(self):

        prods = self.env['select.products.demo'].search([('current_user', '=', self.user_id.id)])

        selecred_colored_prods = self.env['generate.barcode.flag'].search([('color_selected', '=', True)])
        if selecred_colored_prods:
            for i in selecred_colored_prods:
                i.color_selected = False


        sale_id = self.env['sale.order']
        create_so_id = sale_id.create({
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'product_id': prod.id,
                }) for prod in prods.created_product]
        })
        #clear all the table
        for x in prods:
            x.unlink()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Selected Product',
            'res_model': 'sale.order',
            'res_id': create_so_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

