from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    print(">>> get_db: opening session")
    db = SessionLocal()
    try:
        yield db
        print(">>> get_db: after yield, no error")
    except Exception as e:
        print(f">>> get_db: exception caught: {e}")
        raise
    finally:
        print(">>> get_db: closing session")
        db.close()
