# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


user_name = "root"
password = "password"
host = "db"
database_name = "sample_db"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

# We will use the Base class only for the purpose of defining table objects.
# All tables will be defined via Raw SQL, and we will not take any advantage of the ORM feature.
Base = declarative_base()
Base.query = session.query_property()