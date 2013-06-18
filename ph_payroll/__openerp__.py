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
    'name': 'Payroll',
    'version': '0.1',
    'category': 'Human Resources',
    'complexity': "normal",
    'description': """
Generic Payroll System
======================

    * Employee Details
    * Employee Contracts
    * Passport based Contract
    * Allowances / Deductions
    * Allow to configure Basic / Grows / Net Salary
    * Employee Payslip
    * Monthly Payroll Register
    * Integrated with Holiday Management""",
    'author': 'Mederic Roy F. Beldia',
    'website': 'twocngdagz@yahoo.com',
    'depends': ['base','ph_human_resource'],
    'init_xml': [],
    'update_xml': [
        'security/ph_payroll_security.xml',
        'security/ir.model.access.csv',
        'report/report_sample.xml',
        'ph_payroll_view.xml',
        'data/sss_data.xml',
        'data/philhealth_data.xml',
        'data/withholding_data.xml',
        'data/employee_data.xml',
    ],
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
