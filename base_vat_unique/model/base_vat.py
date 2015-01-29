# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#
#    Coded by: Luis Torres (luis_t@vauxoo.com)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
'''
This file add a constraint to unique vat.
'''
from openerp.osv import osv
from openerp.tools.translate import _


class res_partner(osv.Model):
    '''
    Inherit res.partner to added constraint to unique vat of partner
    '''
    _inherit = 'res.partner'

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if not default.get('name', False):
            default.update({'vat': False})
        return super(res_partner, self).copy(
            cr, uid, id, default, context=context)

    def _check_unique_vat(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.vat:
                partner_ids = self.search(
                    cr, uid, [('vat', '=', partner.vat),
                              ('id', '!=', partner.id)], context=context)
                for partner2 in self.browse(
                        cr, uid, partner_ids, context=context):
                    if not (
                        (partner.parent_id and (
                            (partner.parent_id == partner2.parent_id) or (
                                partner.parent_id.id == partner2.id))) or (
                            partner2.id in [
                                child.id for child in partner.child_ids])):
                        return False
        return True

    _constraints = [
        (_check_unique_vat, _('Error! Specified VAT Number already '
         'exists for any other registered partner.'), ['vat'])]
