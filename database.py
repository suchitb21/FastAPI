#suchit123 is the password
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker,Session
from typing import Generator

'''
engine = create_engine("mysql+pymysql://user:password@host:port/database_name")
'''
 
engine=create_engine('postgresql://postgres:suchit123@localhost/pizza_delivery'
                     , echo=True
 )

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db() -> Generator[Session, None , None ]:
    db = SessionLocal() #new session for each request
    try:
        yield db
    finally:
        db.close() #close session when req is finished

def create_db_tables():
    print("creating database tables....")
    Base.metadata.create_all(bind=engine)
    print("Database tables created/checked")