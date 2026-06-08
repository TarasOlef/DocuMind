from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Metadata from this class will be used by Alembic for migrations.
    """
    pass
