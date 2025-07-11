from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from . config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://username:<your_password>@ip-address/hostname/database_name"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', dbname= 'fastapicw', user='postgres', password = 'akhila@525', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database cconnection was successful!!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("error", error)
#         time.sleep(1)
