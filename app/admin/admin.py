from flask import flash, request, redirect, render_template, current_app, url_for
from flask_admin.form import rules, FormOpts
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import expose
from ..models.software import Software
import wtforms as wf
from flask_admin.babel import gettext
import flask_login as login
from flask_admin.form.widgets import DatePickerWidget
from datetime import date, datetime
from flask_admin.model import typefmt
from ..models.users import User, Permission, Role
from ..models.search_logs import SoftwareAccess
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_admin.actions import action
from flask_admin.helpers import is_form_submitted
from wtforms.widgets import TextArea
from wtforms import TextAreaField
import warnings


def date_format(view, value):
    return value.strftime('%Y-%m-%d %H:%M%p')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        date: date_format
    })


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class SoftwareView(ModelView):

    list_template = 'admin/custom_list.html'

    column_type_formatters = MY_DEFAULT_FORMATTERS  # format dateTime without time

    # Columns (in list view):
    # -----------------------
    column_list = ['added_by_name', 'software_name', 'last_updated', 'domain', 'is_pending']
    # column_exclude_list = ['description', 'long_description', 'date']

    column_labels = {
        'added_by_name': 'Added By',
        'is_pending': 'Pending',
    }

    column_filters = ['added_by_name', 'software_name', 'domain', 'is_pending']

    column_searchable_list = ('software_name', 'description')
    # column_editable_list = ['name', ]  # inline editing, has BUG, first ele


    # Others:
    # -------
    # can_create = True
    # can_edit = True
    # can_delete = False
    # page_size = 20  # the number of entries to display on the list view
    can_view_details = True
    can_export = True
    extra = None

    # list_template = 'admin/list.html'
    # create_template = 'create.html'
    edit_template = 'admin/custom_edit.html'

    # create_modal = True
    # edit_modal = True

    # Form options:
    # -------------
    form_excluded_columns = ['languages_lower']

    # form_choices = {        # is select
    #     'ui': [('Yes', 'Yes'), ('No', 'No')]
    # }

    # *** Rename tags here
    form_args = dict(
        added_by_name={'label': 'Name'},
        added_by_email={'label': 'Email'},
        is_SW_owner={'label': 'Are you the Software Owner'},
        mm_features={'label': ''},  # remove label
        # mm_features.qm_mm={'label': 'QM/MM'},  # not here, in form_subdocument
        qm_features={'label': ''},
        is_pending={'label': 'Pending'},
        required_citation={'label': 'Requested Citations(s)'},
        # changes how the input is parsed by strptime (12 hour time)
        # date_of_latest_version={'format': '%Y-%m-%d %I:%M %p'}

    )

    form_widget_args = dict(
        description={'rows': 4, 'style': 'color: black'},
        long_description={'rows': 10, 'style': 'color: black'},
        comments={'rows': 4, 'style': 'color: black'},
        date_of_latest_version={   # http://www.daterangepicker.com/#options
            'data-max-date': datetime.now()
            # 'widget': DatePickerWidget(),  # not working
            # 'data-role': 'datepicker',
            # 'data-date-format': '%Y-%m-%d %I:%M %p',  # has to be in both here and in form_args
            # 'data-show-meridian': 'True'
        }
    )

    form_subdocuments = dict(
        mm_features=dict(
            form_args={
                # 'qm_mm': {'label': 'QM/MM'}  # working
            },  # form_args
            form_rules=[
                'ensembles', 'free_energy_methods', 'advanced_sampling_methods',
                'forcefields', 'file_formats', 'qm_mm', 'tags'
              ],
            # form_widget_args={
            #     'tags': {'class': 'selectpicker form-control', 'data-live-search': "true",
            #     'data-actions-box': "true", 'data-size': 7},
            # },
        ),

        qm_features=dict(
            form_args={
            },  # form_args
            form_rules=[
                # 'basis', 'element_coverage', 'other', 'tags'
              ],
        )
    )

    form_overrides = dict(
        # date_of_latest_version=DateTimeField?
        long_description=CKTextAreaField
    )

    # Form display organization rules
    form_create_rules = [
        rules.HTML('<h4>Please fill this form as complete as you can to be accessible through search.</h4>'),
        rules.HTML('<h5>(For any issues submitting this form contact us at info@molssi.org)</h5>'),
        rules.HTML('<hr>'),

        rules.Header('Your Information'),
        rules.HTML('<h6>Your information will not be public. '
                   'We will use it to contact you if we have questions about your submission, '
                   'or want to clarify something.</h6>'),
        rules.FieldSet(('added_by_name', 'added_by_email', 'is_SW_owner')),
        rules.HTML('<hr>'),

        rules.Header('Availability'),
        'software_name', 'official_website',
        'license', 'price', 'latest_version', 'date_of_latest_version',
        'principal_contact_name', 'principal_contact_email',
        rules.HTML('<hr>'),

        rules.Header('More Details'),
        'description', 'long_description',
        'required_citation', 'languages', 'compilers', 'gui',
        rules.HTML('<hr>'),

        rules.Header('Software Engineering'),
        'source_code_link', 'executables', 'code_management',
        'continuous_integration', 'number_of_tests', 'test_coverage',
        rules.HTML('<hr>'),

        rules.Header('Performance'),
        'parallel', 'gpu', 'knl_optimized',
        rules.HTML('<hr>'),

        rules.Header('Support Links'),
        'support_line', 'documentation', 'number_of_tutorials',
        'wiki', 'forum', 'mail_list',
        rules.HTML('<hr>'),

        'domain',
        rules.Header('MM Features'), 'mm_features',
        rules.Header('QM Features'), 'qm_features',
        rules.HTML('<hr>'),

        rules.HTML('<h3>Do you have any comments or any other information?</h3>'),
        'comments',
        rules.HTML('<hr>'),

        'is_pending',
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    def scaffold_form(self):
        form_class = super(SoftwareView, self).scaffold_form()
        form_class.last_updated_by = ''  # mongoengine requires value for Strings, no None
        # form_class.extra = wf.SelectField('Extra', choices=[('c', 'c'),
        #                       ('cpp', 'CPP'), ('py', 'Python')])
        # form_class.tests = wf.DecimalField('Number of Tests')
        return form_class

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.can(Permission.MODERATE)

    # @action('get_edit_url', 'Edit URL', 'Get a private edit link')
    # def get_edit_url(self, ids):
    #     try:
    #         print('Id is: ', ids)
    #         url = 'admin/software/' + self.generate_software_id_token(ids)
    #         flash('Private URL to edit this software: ' + url)
    #
    #     except Exception as ex:
    #         if not self.handle_view_exception(ex):
    #             raise
    #
    #         flash(gettext('Failed to generate URL. %(error)s', error=str(ex)), 'error')

    def generate_software_id_token(self, id, expiration=3600*24*30):
        """Generate a token safe for URL
            Id: the id of the software in the DB
            expiration: in number of seconds (default to a month)
        """

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(str(id), salt=current_app.config['EDIT_SOFTWARE_SALT'])  # .decode('utf-8')

    def confirm_software_id_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(
                token,  # .encode('utf-8'),
                salt=current_app.config['EDIT_SOFTWARE_SALT'],
                max_age=3600*24*30
            )
        except:
            return False

        return id

class SoftwareViewPublic(SoftwareView):
    """
        View to submit Software by the public.
        marked with is_pending=True for review
    """
    can_create = False
    can_edit = False
    can_delete = False

    form_create_rules = SoftwareView.form_create_rules[:-1]  # without pending checkbox

    extra_css = ['/static/css/custom_admin.css']

    @expose('/', methods=('GET', 'POST'))
    def create_view(self):
        """customize the create view"""

        return_url = '/'

        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            model = self.create_model(form)

            if model:
                # flash('Software was successfully submitted.', 'success')
                return redirect(url_for('submit_software.success', software_id=model.id))
        elif is_form_submitted():
            flash('Some fields are missing', 'error')

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_create_rules)

        return self.render('admin/custom_create.html',
                           # model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    @expose('/edit/<token>', methods=('GET', 'POST'))
    def edit_view_token(self, token):
        """customize the edit view"""

        not_found_url = url_for('submit_software.not_found')
        model = None
        id = self.confirm_software_id_token(token)
        if id:
            model = self.get_one(id)

        if model is None:
            flash('Software does not exist or the URL has expired.', 'error')
            return redirect(not_found_url)

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            # model = self.create_model(form)

            if self.update_model(form, model):
                # flash('Software was successfully submitted.', 'success')
                return redirect(url_for('submit_software.success', software_id=model.id))

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_create_rules)

        return self.render('admin/custom_create.html',
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=not_found_url)

    @expose('/success/<software_id>')
    def success(self, software_id):
        """Return a success page with links to preview and edit software"""

        edit_url = url_for('submit_software.create_view', _external=True) + 'edit/' + \
                                    self.generate_software_id_token(software_id)
        preview_url = url_for('main.software_detail', sw_id=software_id, _external=True)

        return render_template('admin/user_message.html',
                               message='Thank you. The software was submitted successfully.',
                               edit_url=edit_url,
                               preview_url=preview_url)

    @expose('/not_found')
    def not_found(self):
        return render_template('admin/user_message.html', message='')

    def is_accessible(self):
        return True


class UserView(ModelView):

    can_create = False
    column_list = ['full_name', 'email', 'role']
    form_excluded_columns = ['password_hash', 'avatar_hash', 'location', 'confirmed']

    form_widget_args = dict(
        email={'readonly': True},
        full_name={'readonly': True},
        member_since={'readonly': True},
    )

    def is_accessible(self):
        return (login.current_user.is_authenticated
                and login.current_user.can(Permission.ADMIN))


class SoftwareAccessLogsView(ModelView):

    can_create = False
    can_edit = True
    can_export = True
    column_list = ['software', 'access_date', 'ip_address', 'comment']
    # form_excluded_columns = ['ip_address', ]
    column_type_formatters = MY_DEFAULT_FORMATTERS

    form_widget_args = dict(
        software={'readonly': True},  # not working with references
        access_date={'readonly': True},
        ip_address={'readonly': True},
    )
    
    def is_accessible(self):
        return (login.current_user.is_authenticated
                and login.current_user.can(Permission.ADMIN))


def add_admin_views():
    """Register views to admin"""
    from .. import app_admin

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        app_admin.add_view(SoftwareView(Software, name='Software List'))
        app_admin.add_view(UserView(User, name='Users'))
        app_admin.add_view(SoftwareAccessLogsView(SoftwareAccess, name='Search Logs'))
        app_admin.add_view(SoftwareViewPublic(Software, endpoint='submit_software',
                                             name='Submit Software'))
