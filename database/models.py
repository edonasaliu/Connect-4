from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///connect_4_db.sqlite3')
Base = declarative_base()

class SavedMove(Base):
    __tablename__ = 'saved_moves'
    id = Column(Integer, primary_key=True)
    board_state = Column(String, index=True)
    move = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
