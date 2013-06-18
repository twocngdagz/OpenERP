from osv import osv, fields
import addons
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta


class ph_human_resource(osv.osv):
    _name = 'ph.human.resource'
    
    _rec_name = 'fullname'
    
    def _get_fullname(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for name in  self.browse(cr, uid, ids, context):
            if name['suffix'] != False:
                res[name.id] = name['name'] + " " + name['mname'][0:1] + ". " + name['lname'] + " " + name['suffix']
            else:
                res[name.id] = name['name'] + " " + name['mname'][0:1] + ". " + name['lname']
        return res
    
    def _monthdelta(self, cr, uid, d1, d2):
        delta = 0
        while True:
            mdays = calendar.monthrange(d1.year, d1.month)[1]
            d1 += timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
        return delta
    
    def _get_age(self, cr, uid, ids, field, arg,  context=None):
        res = {}
        year = 0
        month = 0
        day = 0
        for record in self.browse(cr, uid, ids, context):
            age_month = None
            if record.hire_date:
                hire_date = record.hire_date
                hire_year = datetime.strptime(hire_date,'%Y-%m-%d').year
                hire_month = datetime.strptime(hire_date,'%Y-%m-%d').month
                hire_day = datetime.strptime(hire_date,'%Y-%m-%d').day
                #month_days = calendar.monthrange(year, month)[1]
                hire_date = date(hire_year, hire_month, hire_day)
                due_date = hire_date + relativedelta(months=+ record.contract_id.duration)
                age_month = self._monthdelta(cr, uid, date.today(), due_date)
            res[record.id] = age_month
        return res
    
    
    def _get_notification(self, cr, uid, ids, field, args, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            if record.age:
                if record.age <= record.contract_id.notify_month:
                    res[record.id] = "old"
                else:
                    res[record.id] = None
            else:
                res[record.id] = "due"        
        return res
    
    def create(self, cr, uid, values, context=None):
        contract_id = values['contract_id']
        if contract_id:
            contract_object = self.pool.get('ph.hr.contract')
            duration = contract_object.read(cr, uid, [contract_id], ['duration'])[0]['duration']
            if values['hire_date']:
                hire_year = datetime.strptime(values['hire_date'],'%Y-%m-%d').year
                hire_month = datetime.strptime(values['hire_date'],'%Y-%m-%d').month
                hire_day = datetime.strptime(values['hire_date'],'%Y-%m-%d').day
                hire_date = date(hire_year, hire_month, hire_day)
                due_date = hire_date + relativedelta(months=+ duration)
                values['due_date'] = due_date
        return super(ph_human_resource, self).create(cr, uid, values, context)
    
    
    def write(self, cr, uid, ids, values, context=None):
        for record in self.browse(cr, uid, ids, context):
            if (values.has_key('contract_id')):
                contract_id = values['contract_id']
            else:
                contract_id = record.contract_id.id
            if contract_id:
                contract_object = self.pool.get('ph.hr.contract')
                duration = contract_object.read(cr, uid, [contract_id], ['duration'])[0]['duration']
                
            if (values.has_key('hire_date')):
                hire_date = values['hire_date']
            else:
                hire_date = record.hire_date
            if hire_date:
                hire_year = datetime.strptime(hire_date,'%Y-%m-%d').year
                hire_month = datetime.strptime(hire_date,'%Y-%m-%d').month
                hire_day = datetime.strptime(hire_date,'%Y-%m-%d').day
                hire_date = date(hire_year, hire_month, hire_day)
                due_date = hire_date + relativedelta(months=+ duration)
                values['due_date'] = due_date
            else:
                values['due_date'] = None
            return super(ph_human_resource,self).write(cr, uid, ids, values)
                    
                
    _columns = {
        'name': fields.char('First Name', size=64, required=True),
        'mname': fields.char('Middle Name', size=64, required=True),
        'lname': fields.char('Last Name', size=64, required=True),
        'fullname': fields.function(_get_fullname, type='char', method=True),
        'sss': fields.char('SSS No', size=64),
        'tin': fields.char('TIN', size=64),
        'hdmf': fields.char('HDMF', size=64),
        'philhealth': fields.char('Philhealth', size=64),
        'home_address': fields.char('Home Address', size=128),
        'permanent_address': fields.char('Permanent Address', size=128),
        'id_no': fields.char('ID No' ,size=64),
        'birth_date': fields.date('Birth Date'),
        'hire_date': fields.date('Hire Date'),
        'due_date': fields.date('Due Date', readonly=True),
        'photo': fields.binary('Photo'),
        'user_id': fields.many2one('res.users', 'User', ondelete='restrict'),
        'active': fields.boolean('Active'),
        'department_id': fields.many2one('ph.hr.department', 'Department', ondelete='restrict'),
        'company_id': fields.many2one('ph.hr.company', 'Company', ondelete='restrict'),
        'gender': fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),
        'mobile_phone': fields.char('Work Mobile', size=32, readonly=False),
        'work_phone': fields.char('Work Mobile', size=32, readonly=False),
        'work_email': fields.char('Work E-mail', size=240),
        'personal_mobile': fields.char('Personal Mobile', size=32),
        'marital': fields.selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
        'telephone': fields.char('Telephone No', size=32, readonly=False),
        'position': fields.char('Work Description', size=32),
        'suffix': fields.char('Suffix', size=32),
        'job_id': fields.many2one('ph.hr.job', 'Job', ondelete='restrict'),
        'age': fields.function(_get_age, type="integer", method=True),
        'contract_id': fields.many2one('ph.hr.contract', 'Employment Contract', required=True),
        'notify': fields.function(_get_notification, type='selection', method=True, selection=[('due','Employee Due!'),
                                ('new',None), ('old','Due date approaching')]),
        
    }
    def _get_photo(self, cr, uid, context=None):
        photo_path = addons.get_module_resource('ph_human_resource','images','photo.png')
        return open(photo_path, 'rb').read().encode('base64')
    
    
    _defaults = {
        'active' : 1,
        'suffix' : None,
        'photo': _get_photo,
    }
ph_human_resource()

class ph_hr_department(osv.osv):
    _name = 'ph.hr.department'
    _columns = {
        'name': fields.char('Department Name', size=64, required=True),
        'active': fields.boolean('Active'),
        'manager_id': fields.many2one('ph.human.resource', 'Manager', ondelete='restrict'),
        'member_ids': fields.one2many('ph.human.resource', 'department_id', 'Members'),
    }
    _defaults = {
        'active' : True,
    }
ph_hr_department()

class ph_hr_company(osv.osv):
    _name = 'ph.hr.company'
    _columns = {
        'name': fields.char('Company Name', size=64, required=True),
        'address': fields.char('Address', size=128),
        'tel_no': fields.char('Telephone No', size=64),
        'fax_no': fields.char('Fax No', size=64),
        'zip_code': fields.char('Zip Code', size=64),
        'email': fields.char('Email Address', size=64),
        'active': fields.boolean('Active'),
        'employee_ids': fields.one2many('ph.human.resource', 'company_id', 'Employees'),
    }
    _defaults = {
        'active' : True,
    }
ph_hr_company()

class ph_hr_job(osv.osv):
    
    def _no_of_employee(self, cr, uid, ids, name, args, context=None):
        res = {}
        for job in self.browse(cr, uid, ids, context=context):
            nb_employees = len(job.employee_ids or [])
            res[job.id] = {
                'no_of_employee': nb_employees,
                'expected_employees': nb_employees + job.no_of_recruitment,
            }
        return res

    def _get_job_position(self, cr, uid, ids, context=None):
        res = []
        for employee in self.pool.get('ph.human.resource').browse(cr, uid, ids, context=context):
            if employee.job_id:
                res.append(employee.job_id.id)
        return res
    
    _name = 'ph.hr.job'
    _columns = {
        'name': fields.char('Job Name', size=128, required=True, select=True),
        'expected_employees': fields.function(_no_of_employee, string='Expected Employees', help='Required number of employees in total for that job.',
            store = {
                'ph.hr.job': (lambda self,cr,uid,ids,c=None: ids, ['no_of_recruitment'], 10),
                'ph.human.resource': (_get_job_position, ['job_id'], 10),
            },
            multi='no_of_employee'),
        'no_of_employee': fields.function(_no_of_employee, string="Number of Employees", help='Number of employees with that job.',
            store = {
                'ph.human.resource': (_get_job_position, ['job_id'], 10),
            },
            multi='no_of_employee'),
        'no_of_recruitment': fields.float('Expected in Recruitment'),
        'employee_ids': fields.one2many('ph.human.resource', 'job_id', 'Employees'),
        'description': fields.text('Job Description'),
        'requirements': fields.text('Requirements'),
        'department_id': fields.many2one('ph.hr.department', 'Department', ondelete='restrict'),
        'company_id': fields.many2one('ph.hr.company', 'Company', ondelete='restrict'),
        'state': fields.selection([('open', 'In Position'),('old', 'Old'),('recruit', 'In Recruitement')], 'State', readonly=True, required=True),
    }
    
    _defaults = {
        'expected_employees': 1,
        'state': 'open',
    }

    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id)', 'The name of the job position must be unique per company!'),
    ]
    
    def on_change_expected_employee(self, cr, uid, ids, no_of_recruitment, no_of_employee, context=None):
        if context is None:
            context = {}
        return {'value': {'expected_employees': no_of_recruitment + no_of_employee}}
    
    def job_old(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'old', 'no_of_recruitment': 0})
        return True

    def job_recruitement(self, cr, uid, ids, *args):
        for job in self.browse(cr, uid, ids):
            no_of_recruitment = job.no_of_recruitment == 0 and 1 or job.no_of_recruitment
            self.write(cr, uid, [job.id], {'state': 'recruit', 'no_of_recruitment': no_of_recruitment})
        return True

    def job_open(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'open', 'no_of_recruitment': 0})
        return True
ph_hr_job()


class ph_hr_contract(osv.osv):
    _name = "ph.hr.contract"
    
    _columns = {
        'name': fields.char('Name', size=32, required=True),
        'duration': fields.integer('Months Duration', required=True),
        'notify_month': fields.integer('Month Notification', required=True),
        'no_work': fields.integer('No of working days', required=True),
        'no_hour': fields.float('No of working hours', required=True),
        'employee_ids': fields.one2many('ph.human.resource', 'contract_id', 'Employee Contract'),
    }
    
    _defaults = {
        'no_hour': 8,
        'no_work': 6,
    }
ph_hr_contract()


class ph_user(osv.osv):
    _name = "res.users"
    _inherit = "res.users"
    
    
    def _get_group(self,cr, uid, context=None):
        dataobj = self.pool.get('ir.model.data')
        result = []
        try:
            dummy,group_id = dataobj.get_object_reference(cr, 1, 'ph_human_resource', 'group_hr_manager')
            result.append(group_id)
        except ValueError:
            # If these groups does not exists anymore
            pass
        return result
    
    
    _defaults = {
        'groups_id': _get_group,
    }
ph_user()







