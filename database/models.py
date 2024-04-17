from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    winner = Column(String)
    moves = relationship("Move", back_populates="game")

class Move(Base):
    __tablename__ = 'moves'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    position = Column(Integer)
    player = Column(String)
    game = relationship("Game", back_populates="moves")

# Configuration
DATABASE_URL = "sqlite:///connect_four.db"  # Example using SQLite
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
