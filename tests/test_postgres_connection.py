"""
from sqlalchemy import create_engine

db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"

db = create_engine(db_string)
"""
import unittest
from shopping import db_session


class TestPostgresConnection(unittest.TestCase):
    def setUp(self):
        db_session.global_init('postgresql://postgres:leonard@localhost')

    def test_create_user(self):
        pass