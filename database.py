from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#on your db url to pass to sqlalchemy engine include the protocol- dbServername - password - @db served port - db name  
URL_DATABASE = 'postgresql://postgres:psql3737@localhost:5432/quiz-application'

engine = create_engine(URL_DATABASE)

#currently autoCommit is not available in the options, check the need and why 
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


