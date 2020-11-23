# -*- coding: utf-8 -*-
{
    'name': "Flag Barcode",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'sale'],

    # always loaded
    'data': [
        'security/flag_barcode_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/flyration_flag.xml',
        'views/affixment_flag.xml',
        'views/entity_flag.xml',
        'views/face_flag.xml',
        'views/image_flag.xml',
        'views/material_flag.xml',
        'views/material_color_flag.xml',
        'views/nomenclature_flag.xml',
        'views/generate_barcode_flag.xml',
        'views/flag_category.xml',
        'views/generate_barcode_lines.xml',
        'views/sh_message_wizard.xml',
        'views/selected_prods.xml',
        'data/sequence.xml',
    ],
    'qweb':['static/src/xml/tree_header_extend.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}