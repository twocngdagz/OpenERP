from datetime import datetime, timedelta
from osv import osv, fields
from tools.translate import _
import calendar
import time
class ph_payroll_schedule(osv.osv):
    _name = 'ph.payroll.schedule'
    
#    def create(self, cr, uid, vals, context=None):
#        dt_to = vals['date_to'][0:10]
#        time_to = vals['date_to'][11:19]
#        notes = vals['notes']
#        lunch = vals['lunch']
#        name = vals['name']
#        dt_from = vals['date_from'][0:10]
#        time_from = vals['date_from'][11:19]
#        date_to = datetime.strptime(dt_to, '%Y-%m-%d')
#        date_from = datetime.strptime(dt_from, '%Y-%m-%d')
#        if vals['date_to'] < vals['date_from']:
#            raise osv.except_osv('Schedule Generation Error', 'End Date < Start Date')
#        while date_from <= date_to:
#            dt_value = datetime.strftime(date_from, '%Y-%m-%d')
#            value  = {
#                          'notes': notes,
#                          'date_from': dt_value + ' ' + time_from,
#                          'date_to': dt_value + ' ' + time_to,
#                          'lunch': lunch,
#                          'name': name,
#                      }
#            user_id = super(ph_payroll_schedule, self).create(cr, uid, value, context)
#            date_from = date_from + timedelta(days=1) 
#        return user_id

#    def write(self, cr, uid, ids, vals, context=None):
#        for record in self.browse(cr, uid, ids, context):
#            print record.starting_date
        

    def _get_starting_date(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            res[record.id] = record.date_from[0:10]
        return res
    
    def _get_ending_date(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            res[record.id] = record.date_to[0:10]
        return res
    
    def _get_starting_time(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            res[record.id] = record.date_from[11:19]
        return res
    
    def _get_ending_time(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            res[record.id] = record.date_to[11:19]
        return res
    
    _columns = {
        'name': fields.char('Description', size=32, required=True, help='Name of the schedule'),
        'state': fields.selection([('draft', 'New'), ('confirm', 'Waiting Approval'), ('refuse', 'Refused'),
            ('validate', 'Approved'), ('cancel', 'Cancelled')],
            'State', readonly=True, help='The state is set to \'Draft\', when a schedule is created.\
            \nThe state is \'Waiting Approval\', when schedule is confirmed by user.\
            \nThe state is \'Refused\', when schedule is refused by manager.\
            \nThe state is \'Approved\', when schedule is approved by manager.'),
        'date_from': fields.datetime('Start Date', readonly=True, states={'draft':[('readonly',False)]}, select=True),
        'date_to': fields.datetime('End Date', readonly=True, states={'draft':[('readonly',False)]}),
        'notes': fields.text('Reasons',readonly=True, states={'draft':[('readonly',False)]}),
        'employee_ids': fields.one2many('ph.human.resource', 'calendar_id', 'Schedule'),
        'lunch': fields.boolean('Lunch Break', help='If true will deduct 1 hour from scheduled time'),
        'monday': fields.boolean('Monday'),
        'tuesday': fields.boolean('Tuesday'),
        'wednesday': fields.boolean('Wednesday'),
        'thursday': fields.boolean('Thursday'),
        'friday': fields.boolean('Friday'),
        'saturday': fields.boolean('Saturday'),
        'sunday': fields.boolean('Sunday'),
        'starting_date': fields.function(_get_starting_date, type='char', method=True),
        'ending_date': fields.function(_get_ending_date, type='char', method=True),
        'starting_time': fields.function(_get_starting_time, type='char', method=True),
        'ending_time': fields.function(_get_ending_time, type='char', method=True),
        'calendar_id': fields.many2one('ph.payroll.calendar', 'Calendar'),
    }
    
    _defaults = {
        'state': 'draft',
        'lunch': 1,
        'monday': 1,
        'tuesday': 1,
        'wednesday': 1,
        'thursday': 1,
        'friday': 1,
    }
ph_payroll_schedule()

class ph_payroll_period(osv.osv):
    _name = 'ph.payroll.period'
    
    _columns = {
        'name': fields.char('Name', size=32, required=True),
        'period_start': fields.date('Period Start', required=True),
        'period_end': fields.date('Period End', required=True),
    }    
ph_payroll_period()

class ph_payroll_calendar(osv.osv):
    _name = 'ph.payroll.calendar'
    
    _columns = {
        'name': fields.char('Name', size=32, required=True),
        'year': fields.integer('Year', required=True),
        'employee_ids':fields.one2many('ph.human.resource', 'calendar_id', 'Employees'),
        'schedule_ids': fields.one2many('ph.payroll.schedule', 'calendar_id', 'Schedules')
    }
ph_payroll_calendar()

class ph_payroll_sss(osv.osv):
    _name = 'ph.payroll.sss'
    
    #def create(self, cr, uid, values, context=None):
    #    self.get_sss(cr, uid, 4000)
    
    _columns = {
        'sss_from': fields.float('From',digits=(12,2)),
        'sss_to': fields.float('To',digits=(12,2)),
        'salary_credit': fields.float('Salary Credit',digits=(12,2)),
        'sss_er': fields.float('ER',digits=(12,2)),
        'sss_ee': fields.float('EE',digits=(12,2)),
        'sss_total': fields.float('Total',digits=(12,2)),
        'ec_er': fields.float('EC-ER',digits=(12,2)),
        'total_er': fields.float('ER',digits=(12,2)),
        'total_ee': fields.float('EE',digits=(12,2)),
        'total_total': fields.float('Total',digits=(12,2)),
        'total_contribution': fields.float('Total Contribution',digits=(12,2)),
    }
    
    def get_sss(self, cr, uid, basic):
        ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, ids):
            if ((basic >= record.sss_from) & (record.sss_to >= basic)):
                return record.sss_ee
        return 0.0
    
    def get_sss_er(self, cr, uid, basic):
        ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, ids):
            if ((basic >= record.sss_from) & (record.sss_to >= basic)):
                return record.sss_er
        return 0.0
            
ph_payroll_sss()

class ph_payroll_philhealth(osv.osv):
    _name = "ph.payroll.philhealth"
    
    _columns = {
        'philhealth_from': fields.float('From', digits=(12,2)),
        'philhealth_to': fields.float('To', digits=(12,2)),
        'salary_base': fields.float('Salary Base', digits=(12,2)),
        'employee': fields.float('Employee Share', digits=(12,2)),
        'employer': fields.float('Employer Share', digits=(12,2)),
        'total': fields.float('Total', digits=(12,2)),
    }
    
    def get_philhealth(self, cr, uid, basic):
        ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, ids):
            if ((basic >= record.philhealth_from) & (record.philhealth_to >= basic)):
                return record.employee
            
    def get_philhealth_er(self, cr, uid, basic):
        ids = self.search(cr, uid, [])
        for record in self.browse(cr, uid, ids):
            if ((basic >= record.philhealth_from) & (record.philhealth_to >= basic)):
                return record.employer
ph_payroll_philhealth()


class ph_payroll_withholding(osv.osv):
    _name = "ph.payroll.withholding"
    
    #def create(self, cr, uid, values, context=None):
        #print self.get_withholding(cr, uid, 36870, 4)
    
    _columns = {
        'name': fields.char('Name', size=32, required=True),
        'deduction_type': fields.selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('semi', 'Semi-Monthly'), ('monthly', 'Monthly')], 'Deduction Type' ),
        'exemption': fields.integer('Exemption'),
        'count': fields.integer('Count'),
        'withholding_line_ids': fields.one2many('ph.payroll.withholding.line','withholding_id', 'Withholding Line')
    }
    
    def get_withholding(self, cr ,uid, taxable, exemption_status, type):
        id = self.search(cr, uid, ['&', ('name', '=', exemption_status), ('deduction_type', '=', type)])
        bracket = 0
        percent_over = 0
        base_tax = 0
        for record in self.browse(cr, uid, id):
            for line in record.withholding_line_ids:
                if (taxable > line.bracket):
                    bracket = line.bracket
                    percent_over = line.percent_over
                    base_tax = line.base_tax
        return ((taxable-bracket) * (percent_over/100)) + base_tax
    
ph_payroll_withholding()

class ph_payroll_withholding_line(osv.osv):
    _name = "ph.payroll.withholding.line"
    
    _columns = {
        'bracket': fields.float('Bracket', digits=(12,2)),
        'percent_over': fields.float('Percentage', digits=(12,2)),
        'base_tax': fields.float('Base Tax', digits=(12,2)),
        'withholding_id': fields.many2one('ph.payroll.withholding', 'Withholding'),
    }
ph_payroll_withholding_line()

class ph_payroll_holiday(osv.osv):
    _name = "ph.payroll.holiday"
    
    _columns = {
        'name': fields.char('Description', size=32, required=True),
        'day': fields.date('Date ', required=True),
        'type': fields.selection([('legal', 'Legal Holiday'), ('special', 'Special Holiday')], 'Type'),
    }
    
    def isHoliday(self, cr, uid, day):
        id = self.search(cr, uid, [('day', '=', day)])
        if (id):
            return True
        return False
        
ph_payroll_holiday()

class ph_payroll_sheet(osv.osv):
    _name = "ph.payroll.sheet"
    
    def create(self, cr, uid, values, context=None):
        id = super(ph_payroll_sheet, self).create(cr, uid, values, context=None)
        self.write(cr, uid, [id], {'state': 'confirm'}, context)
        return id
    
    _columns = {
        'name': fields.char('Name', size=32, required=True),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
        'sheet_line_ids': fields.one2many('ph.payroll.sheet.line', 'paysheet_id', 'Employee Sheet'),
        'state': fields.selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('approved', 'Approved')], 'State', readonly=True, required=True),
        'type': fields.selection([('daily','Daily'),('weekly','Weekly'),('semi','Semi-Monthly'), ('monthly', 'Monthly')], 'Payroll Type'),
        'date': fields.date('Date Process', required=True),
    }
    
    _defaults = {
        'state': 'draft',
        'type': 'semi',
        'date': lambda *a: datetime.now().strftime('%Y-%m-%d'),
    }
    
    def get_year(self, cr, uid, id, context=None):
        for record in self.browse(cr, uid, id):
            return record.date_start[0:4]
        
    
    def compute_sheet(self, cr, uid, ids, context=None):
        basic = 0.0
        employee_object = self.pool.get('ph.human.resource')
        constant_object = self.pool.get('ph.payroll.constant')
        withholding_object = self.pool.get('ph.payroll.withholding')
        philhealth_object = self.pool.get('ph.payroll.philhealth')
        sss_object = self.pool.get('ph.payroll.sss')
        for record in self.browse(cr, uid, ids, context):
            for line in record.sheet_line_ids:
                employee_id = employee_object.search(cr, uid, [('id','=', record.employee_id.id)])
                result = employee_object.read(cr, uid, employee_id, ['basic'])
                basic = result[0]['basic']
ph_payroll_sheet()


class ph_payroll_sheet_line(osv.osv):
    _name = "ph.payroll.sheet.line"
    
    def _get_department(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for i in ids:
            employee_id = self.read(cr, uid, [i], ['employee_id'])[0]['employee_id'][0]
            sql_req = """
            SELECT f.id AS func_id
            FROM ph_human_resource c
                LEFT JOIN ph_hr_department f ON (f.id = c.department_id)
            WHERE
                (c.id = %d)
            """ % (employee_id,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()
            
            if sql_res:
                res[i] = sql_res['func_id']
            else:
                res[i] = False
        return res
    
    def _set_department(self, cr, uid, ids, field_name, field_value, arg, context):
        self.write(cr, uid, id, {'department_id': field_value})
    
    
    def _get_company(self, cr, uid, ids, field_name, arg, context):
        res = {}
        
        for i in ids:
            employee_id = self.read(cr, uid, [i], ['employee_id'])[0]['employee_id'][0]
            sql_req = """
            SELECT f.id AS func_id
            FROM ph_human_resource c
                LEFT JOIN ph_hr_company f ON (f.id = c.company_id)
            WHERE
                (c.id = %d)
            """ % (employee_id,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()
            
            if sql_res:
                res[i] = sql_res['func_id']
            else:
                res[i] = False
        return res
    
    def _set_company(self, cr, uid, ids, field_name, field_value, arg, context):
        self.write(cr, uid, id, {'company_id': field_value})
    
    def _get_netpay(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.net_pay
        return res
    
    def _get_basic(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.basic
        return res
    
    def _get_otpay(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.ot_pay
        return res
    
    def _get_ssscontrib(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.sss_contribution
        return res
    
    def _get_philhealthcontrib(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.philhealth
        return res
    
    def _get_grossincome(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.gross_income
        return res
    
    def _get_pagibigcontrib(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context):
            res[record.id] = record.pag_ibig_contribution
        return res
    
    _columns = {
        'date': fields.date('Processed Date', required=True, readonly=True),
        'employee_id': fields.many2one('ph.human.resource','Employee', states={'approved':[('readonly',True)]}, required=True),
        'basic': fields.float('Basic', digits=(12,12), readonly=True, help="Employee Basic Pay"),
        'regular_hour': fields.float('Reg Hr', digits=(12,2), states={'approved':[('readonly',True)]}, help="Employee Regular Hour Worked"),
        'reg_pay': fields.float('Regular Pay', digits=(12,12), readonly=True,  help="Employee Regular Pay"),
        'nd_hour': fields.float('Night Differential Hr', digits=(12,2), states={'approved':[('readonly',True)]}, help="Employee Night Shift Hour Worked"),
        'nd_pay': fields.float('Night Differential Pay', digits=(12,12), readonly=True, help="Employee Night Differential Pay"),
        'ot_hour': fields.float('Overtime Hr', digits=(12,2), states={'approved':[('readonly',True)]}, help="Employee Overtime Hour Worked"),
        'ot_pay': fields.float('Overtime Pay', digits=(12,12), readonly=True, help="Employee Overtime Pay"),
        'legal_holiday_pay': fields.float('Legal Holiday Pay', digits=(12,12), readonly=True, help="Employee Legal Holiday Hour Worked"),
        'legal_holiday_hour': fields.float('Legal Holiday Hr', digits=(12,2), states={'approved':[('readonly',True)]}, help="Employee Legal Holiday Pay"),
        'special_holiday_pay': fields.float('Special Holiday Pay', digits=(12,12), readonly=True, help="Employee Special Holiday Pay"),
        'special_holiday_hour': fields.float('Special Holiday Hr', digits=(12,2), states={'approved':[('readonly',True)]}, help="Employee Special Holiday Worked"),
        'sss_loan': fields.float('SSS Loan', digits=(12,12), readonly=True, help="Employee SSS Loan"),
        'tax': fields.float('Withholding Tax', digits=(12,12), readonly=True, help="Employee Withholding Tax"),
        'pagibig_loan': fields.float('Pag-ibig Loan', digits=(12,12), readonly=True, help="Employee Pag-ibig Loan"),
        'ca_loan': fields.float('Cash Advance', digits=(12,12), readonly=True, help="Employee Cash Advance"),
        'sss_contribution': fields.float('SSS Contribution', digits=(12,12), readonly=True, help="Employee SSS Contribution"),
        'sss_contribution_er': fields.float('SSS Employer Contribution', digits=(12,12), readonly=True, help="Employer SSS Contribution"),
        'pag_ibig_contribution': fields.float('Pag-ibig Contribution', digits=(12,12), readonly=True, help="Employee Pag-ibig Contribution"),
        'pag_ibig_contribution_er': fields.float('Employer Pag-ibig Contribution', digits=(12,12), readonly=True, help="Employer Pag-ibig Contribution"),
        'philhealth': fields.float('Philhealth', digits=(12,12), readonly=True, help="Employee Philhealth Contribution"),
        'philhealth_er': fields.float('Philhealth Employer', digits=(12,12), readonly=True, help="Employer Philhealth Contribution"),
        'other_contribution': fields.float('Other Contribution', digits=(12,12), readonly=True),
        'cola': fields.float('COLA', digits=(12,12), readonly=True),
        'meal_allow': fields.float('Meal Allowance', digits=(12,12), readonly=True),
        'cloth_allow': fields.float('Clothing Allowance', digits=(12,12), readonly=True),
        'travel_allow': fields.float('Travel Allowance', digits=(12,12), readonly=True),
        'other_allow': fields.float('Other Allowance', digits=(12,12), readonly=True),
        'gross_income': fields.float('Gross Income', digits=(12,2), readonly=True),
        'paysheet_id': fields.many2one('ph.payroll.sheet', 'Payroll Sheet', ondelete='cascade', states={'approved':[('readonly',True)]}, required=True),
        'tardy': fields.float('Late', digits=(12,12), states={'approved':[('readonly',True)]}, help="Number of hours late"),
        'tardy_deduct': fields.float('Tardy Deduction', digits=(12,12), readonly=True),
        'total_allowance': fields.float('Total Allowance', states={'approved':[('readonly',True)]}, digits=(12,12)),
        'taxable_income': fields.float('Taxable Income', states={'approved':[('readonly',True)]}, digits=(12,12)),
        'total_deduction': fields.float('Total Deduction', states={'approved':[('readonly',True)]}, digits=(12,12)),
        'net_pay': fields.float('Net Income', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'state': fields.selection([('draft', 'Draft'), ('confirm','Waiting for Approval'), ('approved', 'Approved')]),
        'leave_nopay': fields.integer('Leave Without Pay', states={'approved':[('readonly',True)]}, help="Number of leave without pay in days"),
        'leave_pay': fields.integer('Leave with Pay', states={'approved':[('readonly',True)]}, help="Number of leave with pay in days"),
        'undertime': fields.float('Undertime', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'undertime_deduct': fields.float('Undertime deduction', digits=(12,12), readonly=True),
        'rest_ot_hour': fields.float('Rest Day OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_ot_pay': fields.float('Rest Day OT pay', digits=(12,12), readonly=True),
        'rest_hour': fields.float('Rest Day hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_pay': fields.float('Rest Day pay', digits=(12,12), readonly=True),
        'rest_nd_hour': fields.float('Rest Day ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_nd_pay': fields.float('Rest Day ND pay', digits=(12,12), readonly=True),
        'special_nd_hour': fields.float('Special Holiday ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'special_nd_pay': fields.float('Special Holiday ND pay', digits=(12,12), readonly=True),
        'special_ot_hour': fields.float('Special Holiday OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'special_ot_pay': fields.float('Special Holiday OT pay', digits=(12,12), readonly=True),
        'legal_nd_hour': fields.float('Legal Holiday ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'legal_nd_pay': fields.float('Leg Holiday ND pay', digits=(12,12), readonly=True),
        'legal_ot_hour': fields.float('Legal Holiday OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'legal_ot_pay': fields.float('Leg Holiday OT pay', digits=(12,12), readonly=True),
        'daily_rate': fields.float('Daily Rate', digits=(12,12), readonly=True),
        'hour_rate': fields.float('Hour Rate', digits=(12,12), readonly=True),
        'minute_rate': fields.float('Minute Rate', digits=(12,12),readonly=True),
        'rest_special_hour': fields.float('Special/Rest Day hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_special_pay': fields.float('Special/Rest Day pay', digits=(12,12), readonly=True),
        'rest_special_ot_hour': fields.float('Special/Rest Day OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_special_ot_pay': fields.float('Special/Rest Day OT pay', digits=(12,12), readonly=True),
        'rest_special_nd_hour': fields.float('Special/Rest Day ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_special_nd_pay': fields.float('Special/Rest Day ND pay', digits=(12,12), readonly=True),
        'rest_legal_hour': fields.float('Legal/Rest Day hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_legal_pay': fields.float('Legal/Rest Day pay', digits=(12,12), readonly=True),
        'rest_legal_ot_hour': fields.float('Legal/Rest Day OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_legal_ot_pay': fields.float('Legal/Rest Day OT pay', digits=(12,12), readonly=True),
        'rest_legal_nd_hour': fields.float('Legal/Rest Day ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_legal_nd_pay': fields.float('Legal/Rest Day ND pay', digits=(12,12), readonly=True),
        'rest_legal_ot_nd_hour': fields.float('Legal/Rest Day ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_legal_ot_nd_pay': fields.float('Legal/Rest Day ND pay', digits=(12,12), readonly=True),
        'rest_special_ot_nd_hour': fields.float('Legal/Rest Day ND hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'rest_special_ot_nd_pay': fields.float('Legal/Rest Day ND pay', digits=(12,12), readonly=True),
        'legal_nd_ot_hour': fields.float('Legal ND OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'legal_nd_ot_pay': fields.float('Legal ND OT pay', digits=(12,12), readonly=True),
        'special_nd_ot_hour': fields.float('Special ND OT hr', states={'approved':[('readonly',True)]}, digits=(12,2)),
        'special_nd_ot_pay': fields.float('Special ND OT pay', digits=(12,12), readonly=True),
        'department_id': fields.function(_get_department, fnct_inv=_set_department, type="many2one", obj="ph.hr.department", method="True", string="Department", store=True),
        'company_id': fields.function(_get_company, fnct_inv=_set_company, type="many2one", obj="ph.hr.company", method="True", string="Company", store=True),
        'display_net_pay': fields.function(_get_netpay, type='float', digits=(12,2), method=True, string="Net Pay"),
        'display_basic': fields.function(_get_basic, type='float', digits=(12,2), method=True, string="Basic"),
        'display_ot_pay': fields.function(_get_otpay, type='float', digits=(12,2), method=True, string="OT Pay"),
        'sss_contrib': fields.function(_get_ssscontrib, type='float', digits=(12,2), method=True, string="SSS"),
        'philhealth_contrib': fields.function(_get_philhealthcontrib, type='float', digits=(12,2), method=True, string="Philhealth"),
        'pagibig_contrib' : fields.function(_get_pagibigcontrib, type='float', digits=(12,2), method=True, string="Pag-ibig"),
        'gross': fields.function(_get_grossincome, type='float', digits=(12,2), method=True, string="Gross Income"),
        'include_deduction': fields.boolean('Include deduction'),
        'include_other_deduction': fields.boolean('Include other deduction'),
        'include_contribution': fields.boolean('Include contribution'),
        'reg_day': fields.float('Regular Days', digits=(12,2)),
    }
    
    _order = 'date desc'
    
    _defaults = {
        'date': lambda *args: time.strftime('%Y-%m-%d'),
        'state': 'draft',
    }
    
#    def isleap(self, cr, uid, year):
#        if ((year % 4) == 0):
#            if ((year % 100) == 0):
#                if ((year % 400) == 0):
#                    return True
#                else:
#                    return False
#            else:
#                return True
#        else:
#            return False


    
    def compute_sheet(self, cr, uid, ids, context=None):
        basic = 0.0
        regular_hour = 0.0
        reg_day = 0.0
        payroll_sheet_object = self.pool.get('ph.payroll.sheet')
        employee_object = self.pool.get('ph.human.resource')
        constant_object = self.pool.get('ph.payroll.constant')
        withholding_object = self.pool.get('ph.payroll.withholding')
        philhealth_object = self.pool.get('ph.payroll.philhealth')
        sss_object = self.pool.get('ph.payroll.sss')
        withholding_object = self.pool.get('ph.payroll.withholding')
        payroll_constant_object = self.pool.get('ph.payroll.constant')
        for record in self.browse(cr, uid, ids, context):
            year = payroll_sheet_object.get_year(cr, uid, [record.paysheet_id.id])
            employee_id = employee_object.search(cr, uid, [('id','=', record.employee_id.id)])
            result = employee_object.read(cr, uid, employee_id, ['basic','cola','sss_contrib','sss_contrib_er',
                                                                 'pagibig_contrib','pagibig_contrib_er','philhealth_contrib','philhealth_contrib_er',
                                                                 'other_contrib','meal_allowance','cloth_allowance',
                                                                 'travel_allowance','other_allowance','sss_loan',
                                                                 'pagibig_loan','cash_advance', 'exemption_status','mwe'])
            constant = payroll_constant_object.read(cr, uid, [1], ['ot_percent','nd_percent','legal_percent',
                                                                   'special_percent','rest_percent','rest_legal_percent',
                                                                   'rest_special_percent','rest_nd_percent',
                                                                   'special_nd_percent','special_rest_nd_percent',
                                                                   'legal_nd_percent','legal_rest_nd_percent',
                                                                   'rest_ot_percent','special_ot_percent',
                                                                   'special_rest_ot_percent','legal_ot_percent',
                                                                   'legal_rest_ot_percent','nd_ot','rest_nd_ot',
                                                                   'special_nd_ot','special_rest_nd_ot',
                                                                   'legal_nd_ot','legal_rest_nd_ot'])
            cola = result[0]['cola']
            mwe = result[0]['mwe']
            if (record.paysheet_id.type == 'semi'):
                basic_rate = result[0]['basic']/2
            if (calendar.isleap(int(year))):
                daily_rate = (result[0]['basic'] * 12)/262
            else:
                daily_rate = (result[0]['basic'] * 12)/261                   
            basic_rate = result[0]['basic']
            if mwe:
                if record.employee_id.contract_id:
                    no_hour = record.employee_id.contract_id.no_hour
                    if (record.regular_hour):
                        regular_hour = record.regular_hour              
                        reg_day = record.regular_hour/no_hour
                    else:
                        if record.reg_day:
                            reg_day = record.reg_day
                            regular_hour = record.reg_day * no_hour
                        else:
                            raise osv.except_osv(_('Error !'), _('Regular Hour or Regular day required for Minimum Wage Employee'))
            meal_allow = result[0]['meal_allowance']
            travel_allow = result[0]['travel_allowance']
            cloth_allow = result[0]['cloth_allowance']
            other_allow = result[0]['other_allowance']
            hour_rate = daily_rate/8
            minute_rate = hour_rate/60
            if mwe:
                basic_rate = result[0]['basic']
                daily_rate = basic_rate
                hour_rate = daily_rate/8
                minute_rate = hour_rate/60
            sss_contrib = result[0]['sss_contrib']
            sss_contrib_er = result[0]['sss_contrib_er']
            pagibig_contrib = result[0]['pagibig_contrib']
            pagibig_contrib_er = result[0]['pagibig_contrib_er']
            philhealth_contrib = result[0]['philhealth_contrib']
            philhealth_contrib_er = result[0]['philhealth_contrib_er']
            other_contrib = result[0]['other_contrib']
            ot_pay = record.ot_hour * (constant[0]['ot_percent']/100) * hour_rate
            tardy_deduct = record.tardy * hour_rate
            nd_pay = record.nd_hour * (constant[0]['nd_percent']/100) * hour_rate
            rest_pay = record.rest_hour * (constant[0]['rest_percent']/100) * hour_rate
            rest_ot_pay = record.rest_ot_hour * (constant[0]['rest_ot_percent']/100) * hour_rate
            rest_nd_pay = record.rest_nd_hour * (constant[0]['rest_nd_percent']/100) * hour_rate
            special_holiday_pay = record.special_holiday_hour * (constant[0]['special_percent']/100) * hour_rate
            special_ot_pay = record.special_ot_hour * (constant[0]['special_ot_percent']/100) * hour_rate
            special_nd_pay = record.special_nd_hour * (constant[0]['special_nd_percent']/100) * hour_rate
            legal_holiday_pay = record.legal_holiday_hour * (constant[0]['legal_percent']/100) * hour_rate
            legal_ot_pay = record.legal_ot_hour * (constant[0]['legal_ot_percent']/100) * hour_rate
            legal_nd_pay = record.legal_nd_hour * (constant[0]['legal_nd_percent']/100) * hour_rate
            rest_special_pay = record.rest_special_hour * (constant[0]['rest_special_percent']/100) * hour_rate
            rest_special_ot_pay = record.rest_special_ot_hour * (constant[0]['special_rest_ot_percent']/100) * hour_rate
            rest_special_nd_pay = record.rest_special_nd_hour * (constant[0]['special_rest_nd_percent']/100) * hour_rate
            rest_legal_pay = record.rest_legal_hour * (constant[0]['rest_legal_percent']/100) * hour_rate
            rest_legal_ot_pay = record.rest_legal_ot_hour * (constant[0]['legal_rest_ot_percent']/100) * hour_rate
            rest_legal_nd_pay = record.rest_legal_ot_hour * (constant[0]['legal_rest_nd_percent']/100) * hour_rate
            rest_legal_ot_nd_pay = record.rest_legal_ot_nd_hour * (constant[0]['legal_rest_nd_ot']/100) * hour_rate
            rest_special_ot_nd_pay = record.rest_special_ot_nd_hour * (constant[0]['special_rest_nd_ot']/100) * hour_rate
            legal_nd_ot_pay = record.legal_nd_ot_hour * (constant[0]['legal_nd_ot']/100) * hour_rate
            special_nd_ot_pay = record.special_nd_ot_hour * (constant[0]['special_nd_ot']/100) * hour_rate
            undertime_deduct = record.undertime * hour_rate 
            gross_income = basic_rate + ot_pay + nd_pay + rest_pay + rest_ot_pay + rest_nd_pay + special_holiday_pay + special_ot_pay + special_nd_pay + legal_holiday_pay + legal_ot_pay + legal_nd_pay + rest_special_pay + rest_special_ot_pay + rest_special_nd_pay + rest_legal_pay + rest_legal_ot_pay + rest_legal_nd_pay + rest_legal_ot_nd_pay + rest_special_ot_nd_pay + legal_nd_ot_pay + special_nd_ot_pay + meal_allow + travel_allow + cloth_allow + other_allow
            taxable_income = gross_income - sss_contrib - pagibig_contrib - philhealth_contrib - tardy_deduct - undertime_deduct
            sample = result[0]['exemption_status']
            if mwe:
                tax = 0.0
                gross_income = (hour_rate*regular_hour) + ot_pay + nd_pay + rest_pay + rest_ot_pay + rest_nd_pay + special_holiday_pay + special_ot_pay + special_nd_pay + legal_holiday_pay + legal_ot_pay + legal_nd_pay + rest_special_pay + rest_special_ot_pay + rest_special_nd_pay + rest_legal_pay + rest_legal_ot_pay + rest_legal_nd_pay + rest_legal_ot_nd_pay + rest_special_ot_nd_pay + legal_nd_ot_pay + special_nd_ot_pay + meal_allow + travel_allow + cloth_allow + other_allow
                sss_contrib = sss_object.get_sss(cr, uid, gross_income)
                sss_contrib_er = sss_object.get_sss_er(cr, uid, gross_income)
                pagibig_contrib = 100.00
                pagibi_contrib_er = 100.00
                philhealth_contrib = philhealth_object.get_philhealth(cr, uid, gross_income)
                philhealth_contrib_er = philhealth_object.get_philhealth_er(cr, uid, gross_income)
                taxable_income = gross_income - sss_contrib - pagibig_contrib - philhealth_contrib - tardy_deduct - undertime_deduct
            else:
                tax = withholding_object.get_withholding(cr, uid, taxable_income, sample, record.paysheet_id.type)
            
            income = taxable_income - result[0]['sss_loan']-result[0]['pagibig_loan']-result[0]['cash_advance']-tax
            val = { 'basic' : result[0]['basic'],
                    'cola' : result[0]['cola'],
                    'sss_contribution' : sss_contrib,
                    'sss_contribution_er': sss_contrib_er,
                    'pag_ibig_contribution' : pagibig_contrib,
                    'pab_ibig_contribution_er': pagibig_contrib_er,
                    'philhealth' : philhealth_contrib,
                    'philhealth_er': philhealth_contrib_er,
                    'other_contribution' : other_contrib,
                    'meal_allow' : meal_allow,
                    'cloth_allow' : cloth_allow,
                    'travel_allow' : travel_allow,
                    'other_allow' : other_allow,
                    'sss_loan' : result[0]['sss_loan'],
                    'pagibig_loan' : result[0]['pagibig_loan'],
                    'ca_loan' : result[0]['cash_advance'],
                    'reg_pay': basic_rate,
                    'ot_pay': ot_pay,
                    'daily_rate': daily_rate,
                    'hour_rate': hour_rate,
                    'minute_rate': minute_rate,
                    'tardy_deduct': tardy_deduct,
                    'nd_pay': nd_pay,
                    'rest_pay': rest_pay,
                    'rest_ot_pay': rest_ot_pay,
                    'rest_nd_pay': rest_nd_pay,
                    'special_holiday_pay': special_holiday_pay,
                    'special_ot_pay': special_ot_pay,
                    'special_nd_pay': special_nd_pay,
                    'legal_holiday_pay': legal_holiday_pay,
                    'legal_ot_pay': legal_ot_pay,
                    'legal_nd_pay': legal_nd_pay,
                    'rest_special_pay': rest_special_pay,
                    'rest_special_ot_pay': rest_special_ot_pay,
                    'rest_special_nd_pay': rest_special_nd_pay,
                    'rest_legal_pay': rest_legal_pay,
                    'rest_legal_ot_pay': rest_legal_ot_pay,
                    'rest_legal_nd_pay': rest_legal_nd_pay,
                    'rest_legal_ot_nd_pay': rest_legal_ot_nd_pay,
                    'rest_special_ot_nd_pay': rest_special_ot_nd_pay,
                    'legal_nd_ot_pay': legal_nd_ot_pay,
                    'special_nd_ot_pay': special_nd_ot_pay,
                    'undertime_deduct': undertime_deduct,
                    'gross_income': gross_income,
                    'taxable_income': taxable_income,
                    'tax': tax,
                    'net_pay': income,
                    'reg_day': reg_day,
                    'regular_hour': regular_hour,
                  }
            self.write(cr, uid, record.id, val)
    
    
    def onchange_employee_id(self, cr, uid, ids, employee_id):
        values = {}
        attendance_object = self.pool.get('ph.payroll.attendance')
        late_hour = 0.0
        under_hour = 0.0
        total_hour = 0.0
        ot_hour = 0.0
        nd_hour = 0.0
        if employee_id:
            employee_object = self.pool.get('ph.human.resource')       
            result = employee_object.read(cr, uid, employee_id, ['basic'])
            values['basic'] = result['basic']
        attendance_ids = attendance_object.search(cr, uid, [('id','=', employee_id)])
        if attendance_ids:
            for attendance in attendance_object.browse(cr, uid, attendance_ids):
                if attendance.late_hour:
                    late_hour += attendance.late_hour
                if attendance.hours_worked:
                    total_hour += attendance.hours_worked
                if attendance.ot_hour:
                    ot_hour += attendance.ot_hour
                if attendance.nd_hour:
                    nd_hour += attendance.nd_hour
                if attendance.under_hour:
                    under_hour += attendance.under_hour
        values['nd_hour'] = nd_hour
        values['ot_hour'] = ot_hour
        values['tardy'] = late_hour
        values['regular_hour'] = total_hour
        values['undertime'] = under_hour
        return {'value': values}
    
    
    def payroll_approved(self, cr, uid, ids, *args):
        return self.write(cr, uid, ids, {'state': 'approved'})
    
    def payroll_confirm(self, cr, uid, ids, *args):
        return self.write(cr, uid, ids, {'state': 'confirm'})
    
    def payroll_draft(self, cr, uid, ids, *args):
        return self.write(cr, uid, ids, {'state': 'draft'})  
ph_payroll_sheet_line()


class ph_payroll_employee_compensation(osv.osv):
    _name = "ph.human.resource"
    _inherit = "ph.human.resource"
    
    def create(self, cr, uid, values, context=None):
        sss_object = self.pool.get('ph.payroll.sss')
        philhealth_object = self.pool.get('ph.payroll.philhealth')
        if (values['mwe']):
            values['sss_contrib'] = sss_object.get_sss(cr, uid, values['basic'])
            values['sss_contrib_employer'] = sss_object.get_sss_er(cr, uid, values['basic'])
            values['philhealth_contrib'] = philhealth_object.get_philhealth(cr, uid, values['basic'])
        id = super(ph_payroll_employee_compensation, self).create(cr, uid, values, context=None)
        return id
    
    def write(self, cr, uid, ids, values, context=None):
        if ids:
            basic = self.read(cr, uid, ids, ['basic'])[0]['basic']
            if (values.has_key('mwe')):
                mwe = values['mwe']
            else:
                mwe = self.read(cr, uid, ids, ['mwe'])[0]['mwe']
            sss_object = self.pool.get('ph.payroll.sss')
            philhealth_object = self.pool.get('ph.payroll.philhealth')
            if (mwe):
                values['sss_contrib'] = 0.0
                values['sss_contrib_employer'] = 0.0
                values['philhealth_contrib'] = 0.0
                values['pagibig_contrib'] = 0.0
            else:
                values['sss_contrib'] = sss_object.get_sss(cr, uid, basic)
                values['sss_contrib_employer'] = sss_object.get_sss_er(cr, uid, basic)
                values['philhealth_contrib'] = philhealth_object.get_philhealth(cr, uid, basic)
                values['pagibig_contrib'] = 100.00
            return super(ph_payroll_employee_compensation, self).write(cr, uid, ids, values, context)
        
        
    def _get_total_allowances(self, cr, uid, ids, field, arg, context=None):
        res = {}
        total = 0.0
        for record in self.browse(cr, uid, ids, context):
            total = record.meal_allowance + record.cloth_allowance + record.travel_allowance + record.other_allowance
            res[record.id] = total
        return res
    
    _columns = {
        'basic': fields.float('Basic Pay', digits=(12,2), required=True),
        'cola': fields.float('COLA', digits=(12,2)),
        'employee_type': fields.selection([('daily', 'Daily Employee'), ('monthly', 'Monthly Employee')], 'Type'),
        'sss_loan': fields.float('SSS Loan', digits=(12,2)),
        'pagibig_loan': fields.float('Pag-ibig Loan', digits=(12,2)),
        'cash_advance': fields.float('Cash Advance', digits=(12,2)),
        'other_loan': fields.float('Other Loan', digits=(12,2)),
        'sss_contrib': fields.float('SSS Contribution Employee', digits=(12,2)),
        'sss_contrib_er': fields.float('SSS Contribution Employer', digis=(12,2)),
        'pagibig_contrib': fields.float('Pag-ibig Contribution', digits=(12,2)),
        'pagibig_contrib_er': fields.float('Pag-ibig Contribution Employer', digits=(12,2)),
        'philhealth_contrib': fields.float('Philhealth Contribution', digits=(12,2)),
        'philhealth_contrib_er': fields.float('Philhealth Contribution Employer', digits=(12,2)),
        'other_contrib': fields.float('Other Contribution', digits=(12,2)),
        'meal_allowance': fields.float('Meal Allowance', digits=(12,2)),
        'cloth_allowance': fields.float('Clothing Allowance', digits=(12,2)),
        'travel_allowance': fields.float('Travel Allowance', digits=(12,2)),
        'other_allowance': fields.float('Other Allowance', digits=(12,2)),
        'total_allowance': fields.function(_get_total_allowances, type='float', method=True),
        'calendar_id': fields.many2one('ph.payroll.calendar', 'Calendar'),
        'exemption_status': fields.selection([('Z', 'Z'), ('S/ME', 'S/ME'), ('ME1/S1', 'ME1/S1'), ('ME2/S2', 'ME2/S2'), ('ME3/S3', 'ME3/S3'), ('ME4/S4', 'ME4/S4')], 'Exemption Status', required=True),
        'mwe': fields.boolean('Min Wage Earner'),
        'allow_ot': fields.boolean('Compute Overtime'),
        'allow_nd': fields.boolean('Compute Undertime'),
    }
    
    _defaults = {
        'basic': 0.0,
        'pagibig_contrib' : 100.00,
        'pagibig_contrib_er': 100.00,
        'mwe': 1,
        'exemption_status' : 'Z',
    }
ph_payroll_employee_compensation()



class  ph_payroll_constant(osv.osv):
    _name = "ph.payroll.constant"
    
    _columns = {
        'ot_percent': fields.float('Overtime %', digits=(12,2), help="percentage to be added in basic pay during overtime"),
        'nd_percent': fields.float('Night Differential %', digits=(12,2), help="percentage to be added in basic pay during night differential"),
        'legal_percent': fields.float('Legal Holiday %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday"),
        'special_percent': fields.float('Special Holiday %', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday"),
        'rest_percent': fields.float('Rest Day %', digits=(12,2), help="percentage to be added in basic pay when employee worked during his/her rest day"),
        'rest_legal_percent': fields.float('Legal Holiday & Rest Day %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holidays and rest day"),
        'rest_special_percent': fields.float('Special Holiday % Rest Day %', help="percentage to be added in basic pay when employee worked during special holiday and rest day"),
        'rest_nd_percent': fields.float('Rest Day & Night Differential %', digits=(12,2), help="percentage to be added in basic pay when employee worked during rest day and night shift"),
        'special_nd_percent': fields.float('Special Holiday & Night Differential', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday and night shift"),
        'special_rest_nd_percent': fields.float('Special Holiday, Rest Day & Night Differential %', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday, rest day, and night shift"),
        'legal_nd_percent': fields.float('Legal Holiday & Night Differential %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday and nigh shift"),
        'legal_rest_nd_percent': fields.float('Legal Holiday, Rest Day & Night Differential %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday, rest day & night shift"),
        'rest_ot_percent':fields.float('Rest Day & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during his/her rest day and overtime"),
        'special_ot_percent': fields.float('Special Holiday & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday and overtime"),
        'special_rest_ot_percent': fields.float('Special Holiday, Rest Day & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday, rest day and overtime"),
        'legal_ot_percent': fields.float('Legal Holiday & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday and overtime"),
        'legal_rest_ot_percent': fields.float('Legal Holiday, Rest Day & Overtime', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday, rest day & overtime"),
        'nd_ot': fields.float('Night Differential & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during night shift and overtime"),
        'rest_nd_ot': fields.float('Rest Day, Night Differential & Overtime', digits=(12,2), help="percentage to be added in basic pay when employee worked during rest day, night shift & overtime"),
        'special_nd_ot': fields.float('Special Holiday, Night Differential & Overtime', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday, night shift and overtime"),
        'special_rest_nd_ot': fields.float('Special Holiday, Night Differential, Rest Day & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during special holiday, rest day, night shift & overtime"),
        'legal_nd_ot': fields.float('Legal Holiday, Night Shift Differential & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holiday, night shift and overtime"),
        'legal_rest_nd_ot': fields.float('Legal Holiday, Rest Day, Night Differenttial & Overtime %', digits=(12,2), help="percentage to be added in basic pay when employee worked during legal holida, rest day, night shift and overtime"),  
    }
ph_payroll_constant()
  
class ph_payroll_attendance(osv.osv):
    _name = "ph.payroll.attendance"
    
    def _get_department(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for i in ids:
            employee_id = self.read(cr, uid, [i], ['employee_id'])[0]['employee_id'][0]
            sql_req = """
            SELECT f.id AS func_id
            FROM ph_human_resource c
                LEFT JOIN ph_hr_department f ON (f.id = c.department_id)
            WHERE
                (c.id = %d)
            """ % (employee_id,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()
            
            if sql_res:
                res[i] = sql_res['func_id']
            else:
                res[i] = False
        return res
    
    def _set_department(self, cr, uid, ids, field_name, field_value, arg, context):
        self.write(cr, uid, id, {'department_id': field_value})
    
    def _get_company(self, cr, uid, ids, field_name, arg, context):
        res = {}
        
        for i in ids:
            employee_id = self.read(cr, uid, [i], ['employee_id'])[0]['employee_id'][0]
            sql_req = """
            SELECT f.id AS func_id
            FROM ph_human_resource c
                LEFT JOIN ph_hr_company f ON (f.id = c.company_id)
            WHERE
                (c.id = %d)
            """ % (employee_id,)
            cr.execute(sql_req)
            sql_res = cr.dictfetchone()
            
            if sql_res:
                res[i] = sql_res['func_id']
            else:
                res[i] = False
        return res
    
    def _set_company(self, cr, uid, ids, field_name, field_value, arg, context):
        self.write(cr, uid, id, {'company_id': field_value})
    
    
    def get_float_time(self, cr, uid, tdelta):
        list = str.split(str(tdelta), ',')
        if len(list) == 1:
            list = list[0]
        else:
            list = list[1]
        tlist = str.split(str(list), ':')
        thour = float(tlist[0])
        tmin = float(tlist[1])
        tsec = float(tlist[2])
        total = thour + tmin/60 + ((tsec > 30) and float(1)/60 or 0)
        return total
    
    def time_diff(self, cr, uid, time1, time2):
        tformat = '%H:%M:%S'
        t1 = datetime.strptime(time1, tformat)
        t2 = datetime.strptime(time2, tformat)
        tdelta = t1 - t2
        tlist = str.split(str(tdelta), ':')
        thour = float(tlist[0])
        tmin = float(tlist[1])
        tsec = float(tlist[2])
        total = thour + tmin/60 + ((tsec > 30) and float(1)/60 or 0)
        return total
    
    def get_nd(self, cr, uid, time_in, time_out):
        format = '%Y-%m-%d %H:%M:%S'
        total = 0.0
        one_day  = timedelta(days=1)
        three_forth_day = timedelta(hours=16)
        one_forth_day = timedelta(hours=8)
        actual_date_in = time_in + one_forth_day
        
        time_in = time_in + one_forth_day
        time_out = time_out + one_forth_day
             
        nd_start_today = datetime.strptime(actual_date_in.date().strftime('%Y-%m-%d') + ' ' + '22:00:00', format)
        nd_end_today = datetime.strptime((actual_date_in+one_day).date().strftime('%Y-%m-%d') + ' ' + '6:00:00', format)
        nd_start_yesterday = nd_start_today - one_day
        nd_end_yesterday = nd_start_today - three_forth_day
        
        if (time_in <= nd_end_yesterday and nd_start_yesterday <= time_in):
            total += self.get_float_time(cr, uid, nd_end_yesterday - time_in)
        if (time_out >= nd_start_today and time_out <= nd_end_today):
            total += self.get_float_time(cr, uid, time_out - nd_start_today)
        if (time_in <= nd_start_today) and (time_out >= nd_end_today):
            total += 8.0
        if (time_in >= nd_start_today) and (time_out>=nd_end_today) and (time_in <= nd_end_today):
            total += self.get_float_time(cr, uid, nd_end_today - time_in)
        return total
         
         
    def _get_hours(self, cr, uid, ids, field, arg, context=None):
        rs_data = {}
        format = '%Y-%m-%d %H:%M:%S'
        attendance_ids = self.browse(cr, uid, ids, context)
        for record in attendance_ids:
            res = {}
            if record.in_ > record.out:
                raise osv.except_osv(_('Error !'), _('In date cannot be larger than Out date'))
            no_hour = record.employee_id.contract_id.no_hour
            allow_ot = record.employee_id.allow_ot
            allow_nd = record.employee_id.allow_nd
            schedules = record.employee_id.calendar_id.schedule_ids
            out = datetime.strptime(record.out, format)
            in_ = datetime.strptime(record.in_, format)
            date_in = str.split(record.in_,' ')[0]
            date_out = str.split(record.out, ' ')[0]
            time_in = str.split(record.in_,' ')[1]
            time_out = str.split(record.out,' ')[1]
            interval = out - in_
            list = str.split(str(interval), ',')
            if len(list) == 1:
                res['hours_worked'] = no_hour
            else:
                raise osv.except_osv(_('Warning !'), _('Working hours cannot exceed 24 hrs.'))
            if schedules:
                for schedule in schedules:
                    if ((schedule.starting_date <= date_in) and (date_in <= schedule.ending_date)):
                        if allow_nd:
                            starting_time = datetime.strptime(date_in + ' ' + time_in, format)
                            ending_time = datetime.strptime(date_in + ' ' + time_out, format)
                        else:
                            starting_time = datetime.strptime(date_in + ' ' + schedule.starting_time, format)
                            ending_time = datetime.strptime(date_in + ' ' + schedule.ending_time, format)
                        res['nd_hour'] = self.get_nd(cr, uid, starting_time, ending_time)
                        if (schedule.starting_time < time_in):  #for late                     
                            res['late_hour'] = self.time_diff(cr, uid, time_in, schedule.starting_time)
                            res['hours_worked'] = res['hours_worked'] - res['late_hour']
                        if (schedule.ending_time > time_out):   #undertime  
                            res['under_hour'] = self.time_diff(cr, uid, schedule.ending_time, time_out)
                            res['hours_worked'] = res['hours_worked'] - res['under_hour']
                        if (time_out > schedule.ending_time and allow_ot): #compute overtime
                            res['ot_hour'] = self.time_diff(cr, uid, time_out, schedule.ending_time)
            rs_data[record.id] = res
        return rs_data
    
    _columns = {
        'out': fields.datetime('Out', required=True),
        'in_': fields.datetime('In', required=True),
        'employee_id': fields.many2one('ph.human.resource', 'Employee', ondelete='restrict', required=True),
        'hours_worked': fields.function(_get_hours, multi="hour", type="float", method=True, string="Reg"),
        'late_hour': fields.function(_get_hours, multi="hour", type="float", method=True, string="Late"),
        'under_hour': fields.function(_get_hours, multi="hour", type="float", method=True, string="Undertime"),
        'ot_hour': fields.function(_get_hours, multi="hour", type="float", method=True, string="OT"),
        'nd_hour': fields.function(_get_hours, multi="hour", type="float", method=True, string="ND"),
        'company_id': fields.function(_get_company, fnct_inv=_set_company, type="many2one", obj="ph.hr.company", method="True", string="Company", store=True),
        'department_id': fields.function(_get_department, fnct_inv=_set_department, type="many2one", obj="ph.hr.department", method="True", string="Department", store=True),
    }
    
    _order = 'in_ desc'
ph_payroll_attendance()

