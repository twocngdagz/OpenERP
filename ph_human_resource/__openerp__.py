# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################


{
    'name': 'Human Resource',
    'version': '0.1',
    'category': 'Human Resources',
    'complexity': "normal",
    'description': """
Module for Human Resouce Management
===================================

    You can manage:
    * Employees and hierarchies : You can define your employee with User and display hierarchies
    * HR Departments
    * HR Jobs""",
    'author': 'Mederic Roy F. Beldia',
    'website': 'twocngdagz@yahoo.com',
    'depends': ['base'],
    'init_xml': [],
    'update_xml': [
        'security/ph_human_resource_security.xml',
        'security/ir.model.access.csv',
        'ph_human_resource_view.xml',
    ],
    'demo_xml': [
        'demo/ph_hr_demo.xml',
    ],
    'installable': True,
	'css': ['static/src/css/human_resource.css'],
    'js': ['static/src/js/ph_hr_resource.js'],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
