"""
Database adapter for psycopg2cffi compatibility with SQLAlchemy.
This file helps SQLAlchemy use psycopg2cffi instead of psycopg2.
"""
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

# Register psycopg2cffi as a psycopg2 replacement
try:
    import psycopg2cffi.compat
    psycopg2cffi.compat.register()
except ImportError:
    # If psycopg2cffi is not available, we'll use regular psycopg2
    pass

# Create a custom dialect that will be used by SQLAlchemy
class PGDialect_psycopg2cffi(PGDialect_psycopg2):
    driver = 'psycopg2cffi'

# Register the dialect with SQLAlchemy
from sqlalchemy.dialects import registry
registry.register("postgresql.psycopg2cffi", "app.database", "PGDialect_psycopg2cffi")
