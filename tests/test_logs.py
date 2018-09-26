from flask import current_app
import pytest
from app.models.search_logs import SoftwareAccess, save_access
from app.models.software import Software


@pytest.mark.usefixtures("app", "client")
class TestDatabase(object):
    """
        Testing Log DB CRUD operations
    """

    def test_app_exists(self):
        assert current_app is not None

    def test_db_exit(self):
        SoftwareAccess.objects.delete()
        assert SoftwareAccess.objects().count() == 0

    def test_add_log(self):
        # with context, to be able to use request and session
        with current_app.test_request_context():
            software = Software.objects().first()
            save_access(software=software)

            assert SoftwareAccess.objects().count() != 0
            log = SoftwareAccess.objects().first()
            assert 'access_date' in str(log)
            assert log.software.software_name == software.software_name
