"""
Aligns sqlalchemy's schema for the "views" table with the database.
"""

from sqlalchemy import (Boolean, Column, DateTime, Float, Integer, PrimaryKeyConstraint, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func

Base = declarative_base()


class View(Base):
    """
    DeclarativeMeta class for the views table.

    Arguments:
        Base {DeclarativeMeta} -- Base class for model to inherit.
    """
    __tablename__ = 'views'
    url = Column(Text, unique=True)
    session_id = Column(String)
    last_checkin = Column(DateTime, default=func.now)
    active_users = Column(Integer)
    PrimaryKeyConstraint(url)

    def __repr__(self):
        return "<View(url='{0}', active_users='{1}')>".format(
            self.url, self.active_users)
