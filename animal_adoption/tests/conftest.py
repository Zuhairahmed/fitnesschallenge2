from animal_adoption.models.initialize_db_data import initialize_db
import os
import tempfile
import pytest
from animal_adoption import app, db
from animal_adoption.models.initialize_db_data import initialize_db

@pytest.fixture
def client():
    db_fd, file_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        # setup & populate initial data
        with app.app_context():
            db.create_all()
            initialize_db()

        yield client

    os.close(db_fd)
    os.unlink(file_path)