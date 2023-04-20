from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import SQLALCHEMY_URL

engine = create_engine(SQLALCHEMY_URL)
metadata = MetaData().create_all(engine)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db_session():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
