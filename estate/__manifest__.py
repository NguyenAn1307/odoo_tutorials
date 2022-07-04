# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Real Estate',
    'version' : '1.0',
    'summary': 'The Real Estate Advertisement module',
    'sequence': 0,
    'description': """
    """,
    'category': 'Services',
    'website': 'fb.com/nguyenan1307',
    'depends' : [],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}