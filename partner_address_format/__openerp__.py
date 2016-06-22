# -*- coding: utf-8 -*-
# © 2016 Vauxoo (http://www.vauxoo.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Nhomar Hernandez <nhomar@vauxoo.com>
{
    'name': "Partner Html Address Format",
    'summary': """Customize the way you show the address in html to have a
    proper global way in Odoo to do that.""",
    'author': "Vauxoo",
    'website': "http://www.vauxoo.com",
    'category': 'Base',
    'version': '8.0.0.1.0',
    'depends': [
        # Even if technically we do not need this dependency.
        # It is mandatory to test this behaviour  with Portal
        # module installed and with a regular demo portal which is
        # One of the more freely created users, please in the near
        # future if you find a better way to achieve this remove
        # This dependency and propose a better patch. Remember Porta
        # is autoinstall=True.
        'portal',
    ],
    'data': [
        'views/templates.xml',
        'views/res_company.xml',
        'views/res_country.xml',
        'data/country_data.xml',
        'data/company_data.xml',
    ],
    'demo': [
        'demo/template_demo.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
