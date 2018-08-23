import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    flask_app = create_app('testing')
    app_context = flask_app.app_context()
    app_context.push()
    # fill_db()

    yield flask_app

    # clean up
    app_context.pop()


# autouse=True to make it available to all methods implicitly
# but it does not work for fixtures that return value
@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
