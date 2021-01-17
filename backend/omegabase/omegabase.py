"""
Defines the connection to the database for the Omegalearn app.
"""
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.orm import sessionmaker

from omegabase.transactions import (add_view_txn, edit_note_txn, end_call_txn, get_note_txn, get_view_txn,
                                    join_call_txn, leave_call_txn,
                                    remove_view_txn, start_call_txn)

registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                  "CockroachDBDialect")


class Omegabase:
    """
    Wraps the database connection. The class methods wrap transactions.
    """

    def __init__(self, conn_string, max_records=20):
        """
        Establish a connection to the database, creating an Engine instance.

        Arguments:
            conn_string {String} -- CockroachDB connection string.
        """
        self.engine = create_engine(conn_string, convert_unicode=True)
        self.connection_string = conn_string
        self.max_records = max_records

    def start_call(self, url, session_id):
        """
        Wraps a `run_transaction` call that starts a ride.

        Arguments:
            url
            session_id
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: start_call_txn(session, url, session_id))

    def join_call(self, url):
        """
        Wraps a `run_transaction` call that adds a new url or increments the user count of a url.

        Arguments:
            url
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: join_call_txn(session, url))

    def leave_call(self, url):
        """
        Wraps a `run_transaction` call that decrements the user count of a url.

        Arguments:
            url
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: leave_call_txn(session, url))

    def end_call(self, url):
        """
        Wraps a `run_transaction` call that ends the call.

        Clears the session_id

        Arguments:
            url
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: end_ride_txn(session, url))

    def remove_view(self, url):
        """
        Wraps a `run_transaction` call that "removes" a url.

        Arguments:
            url
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: remove_view_txn(session, url))

    def add_view(self, url):
        """
        Wraps a `run_transaction` call that adds a view.

        Arguments:
            url {Text}
        """
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: add_view_txn(session, url))

    def get_view(self, url):
        """
        Get a single view from its url.
        """
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: get_view_txn(session, url))

    def get_note(self, url):
        """
        Get note from url
        """
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: get_note_txn(session, url))

    def edit_note(self, url, content):
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: edit_note_txn(session, url, content))

    def show_tables(self):
        """
        Returns:
            List -- A list of tables in the database it's connected to.
        """
        return self.engine.table_names()
