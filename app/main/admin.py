from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView

from ..models.library import Library


class LibraryView(ModelView):
    column_filters = ['name']

    column_searchable_list = ('name',)


# Register views to admin
def add_admin_views():
    from .. import admin as app_admin
    app_admin.add_view(LibraryView(Library))
