"""
Defines the transactions that are performed by movr.

This is where the python code meets the database.
"""

from sqlalchemy.sql.expression import func

from omegabase.models import View


def start_call_txn(session, url, session_id):
    """
    Start a call

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {Text}
        session_id {String} -- The session_id used by OpenTok
    """
    # find the row where we want to start the call.
    # SELECT * FROM views WHERE url = <url> AND session_id = NULL
    #         LIMIT 1;
    view = session.query(View).filter(View.url == url).filter(
        View.session_id == NULL).first()

    if view is None:
        return None

    # perform the update
    # UPDATE views SET session_id = session_id, last_checkin = now()
    #               WHERE url = <url> AND session_id = NULL
    #               LIMIT 1;
    view.session_id = session_id
    view.last_checkin = func.now()

    return True  # Just making it explicit that this worked.


def join_call_txn(session, url):
    """
    Update a row of the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {String}

    Returns:
        {Boolean} -- True if the call was joined.
    """
    # find the row
    # SELECT * FROM views WHERE url = <url>;
    view = session.query(View).filter(View.url == url).first()

    if view is None:
        return False

    # perform the update on the row that matches the query above.
    # UPDATE views SET active_users = active_users + 1, last_checkin = now()
    #               WHERE url = <url>
    view.active_users = view.active_users + 1
    view.last_checkin = func.now()

    return True  # Just making it explicit that this worked.


def leave_call_txn(session, url):
    """
    Update a row of the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {String}

    Returns:
        {Boolean} -- True if the call ended.
    """
    # find the row
    # SELECT * FROM views WHERE url = <url>;
    view = session.query(View).filter(View.url == url).first()

    if view is None:
        return False

    # perform the update on the row that matches the query above.
    # UPDATE views SET active_users = active_users - 1, last_checkin = now()
    #               WHERE url = <url>
    view.active_users = view.active_users - 1
    view.last_checkin = func.now()

    return True  # Just making it explicit that this worked.


def end_call_txn(session, url):
    """
    Update a row of the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {String}

    Returns:
        {Boolean} -- True if the call ended.
    """
    # find the row
    # SELECT * FROM views WHERE url = <url>;
    view = session.query(View).filter(View.url == url).first()

    if view is None:
        return False

    # perform the update on the row that matches the query above.
    # UPDATE views SET session_id = NULL, last_checkin = now()
    #               WHERE url = <url>
    view.session_id = NULL
    view.last_checkin = func.now()

    return True  # Just making it explicit that this worked.


def add_view_txn(session, url):
    """
    Insert a row into the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {Text}

    Returns:
        url {Text}
    """
    current_time = func.now()  # Current time on database
    new_row = View(url=str(url), last_checkin=current_time)

    # https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.add

    session.add(new_row)

    return True


def remove_view_txn(session, url):
    """
    Deletes a row from the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {Text}

    Returns:
        {None} -- view isn't found
        True {Boolean} -- view is deleted
    """
    # find the row.
    # SELECT * FROM views WHERE url = <url> AND active_users = 0;
    view = session.query(View).filter(View.url == url).filter(
        View.active_users == 0).first()

    if view is None:  # Either view is in use or it's been deleted
        return None

    # View has been found. Delete it.
    # https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.delete

    session.delete(view)

    return True  # Should return True when view is deleted.


def get_views_txn(session, max_records):
    """
    Select all rows of the views table.

    Arguments:
        session {.Session} -- The active session for the database connection.
        max_records {Integer} -- Limits the number of records returned.

    Returns:
        {list} -- A list of dictionaries containing view information.
    """
    # SELECT * FROM views LIMIT max_records;
    views = session.query(View).limit(max_records).all()

    # Return the results in a form that will persist.
    return list(map(lambda view: {'url': view.url,
                                  'session_id': view.session_id,
                                  'last_checkin': view.last_checkin,
                                  'active_users': view.active_users},
                    views))


def get_view_txn(session, url):
    """
    For when you just want a single view.

    Arguments:
        session {.Session} -- The active session for the database connection.
        url {Text}

    Returns:
        {dict} or {None} -- Contains view information or None if no view found.
    """
    # Find the row
    # SELECT * FROM views WHERE url = <url>;
    view = session.query(View).filter(View.url == url).first()

    # Return the row as a dictionary for flask to populate a page.
    if view is None:
        return None

    return {'url': str(view.url),
            'session_id': view.session_id,
            'last_checkin': view.last_checkin,
            'active_users': view.active_users}
