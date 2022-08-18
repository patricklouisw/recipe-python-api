"""
Test custom  Dango management commands.
"""
# Mock behaviour of database
from unittest.mock import patch

# One error when we're trying to connect to db before the db is ready
from psycopg2 import OperationalError as Psycopg2Error

# To call_command that we're testing
from django.core.management import call_command
# Another exception that might be thrown
from django.db.utils import OperationalError
# SimpleTestCase: for test cases that doesn't need to migrate a db
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationalError

        Unit Test ARGS is called from the inside out
        patched_sleep args: time.sleep
        patched_check args: core.management.commands.wait_for_db.Command.check
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
