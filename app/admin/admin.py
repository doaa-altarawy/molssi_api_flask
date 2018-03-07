from flask import flash, request, redirect, render_template
from flask_admin.form import rules, FormOpts
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import expose
from ..models.software import Software
import wtforms as wf
from flask import url_for
from flask_admin.babel import gettext
import flask_login as login
from flask_admin.form.widgets import DatePickerWidget
from datetime import date, datetime
from flask_admin.model import typefmt


def date_format(view, value):
    return value.strftime('%Y-%m-%d')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        date: date_format
    })


class SoftwareView(ModelView):

    column_type_formatters = MY_DEFAULT_FORMATTERS  # format dateTime without time

    # Columns (in list view):
    # -----------------------
    column_list = ['added_by_name', 'software_name', 'domain', 'is_pending']
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
        is_SW_owner={'label': 'Are you Software Owner'},
        mm_features={'label': ''},  # remove label
        # mm_features.qm_mm={'label': 'QM/MM'},  # not here, in form_subdocument
        qm_features={'label': ''},
        is_pending={'label': 'Pending'},
        # changes how the input is parsed by strptime (12 hour time)
        # date_of_latest_version={'format': '%Y-%m-%d %I:%M %p'}

    )

    form_widget_args = dict(
        description={'rows': 4, 'style': 'color: black'},
        long_description={'rows': 10, 'style': 'color: black'},
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

    form_overrides = {
        # 'date_of_latest_version': DateTimeField?
    }

    # Form display organization rules
    form_create_rules = [
        rules.FieldSet(('added_by_name', 'added_by_email', 'is_SW_owner'), 'Your Information'),
        rules.HTML('<hr>'),

        rules.Header('Availability'),
        'software_name', 'official_website',
        'license', 'price', 'latest_version', 'date_of_latest_version',
        'principal_contact_name', 'principal_contact_email',
        rules.HTML('<hr>'),

        rules.Header('More Details'),
        'description', 'long_description', 'comments',
        'required_citation', 'languages', 'compilers', 'ui',
        rules.HTML('<hr>'),

        rules.Header('Software Engineering'),
        'source_code', 'executables', 'code_management',
        'continuous_integration', 'tests',
        rules.HTML('<hr>'),

        rules.Header('Performance'),
        'parallel', 'gpu', 'knl',
        rules.HTML('<hr>'),

        rules.Header('Support Links'),
        'support_line', 'documentation', 'number_of_tutorials',
        'wiki', 'forum', 'mail_list',
        rules.HTML('<hr>'),

        'domain',
        rules.Header('MM Features'), 'mm_features',
        rules.Header('QM Features'), 'qm_features',
        'is_pending',
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    def scaffold_form(self):
        form_class = super(SoftwareView, self).scaffold_form()
        # form_class.extra = wf.SelectField('Extra', choices=[('c', 'c'),
        #                       ('cpp', 'CPP'), ('py', 'Python')])
        # form_class.tests = wf.DecimalField('Number of Tests')
        return form_class

    def is_accessible(self):
        return login.current_user.is_authenticated


class SoftwareViewPublic(SoftwareView):
    """
        View to submit Software by the public.
        marked with is_pending=True for review
    """
    can_create = True
    can_edit = True
    can_delete = False

    form_create_rules = SoftwareView.form_create_rules[:-1]

    extra_css = ['/static/css/custom_admin.css']

    @expose('/', methods=('GET', 'POST'))
    def create_view(self):
        """customize the view"""

        return_url = '/'

        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            model = self.create_model(form)

            if model:
                flash(gettext('Record was successfully created.'), 'success')
                return redirect('/success')

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_create_rules)

        return self.render('admin/custom_create.html',
                           # model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    @expose('/success')
    def sucess(self):
        return render_template('software_added_success.html')


# Register views to admin
def add_admin_views():
    from .. import app_admin
    app_admin.add_view(SoftwareView(Software, name='CMS Software DB (private)'))
    app_admin.add_view(SoftwareViewPublic(Software, endpoint='submit_software',
                                         name='Submit Software (public)'))

