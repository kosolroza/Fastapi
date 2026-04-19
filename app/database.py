from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Roza231105@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


# Create dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
        