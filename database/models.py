from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///connect_4_db.sqlite3')
Base = declarative_base()

class SavedMove(Base):
    """
    Represents a saved move in the Connect-4 game.

    Attributes:
        id (int): The unique identifier for the saved move.
        board_state (str): The state of the game board at the time the move was saved.
        move (str): The move that was made and saved.
    """
    __tablename__ = 'saved_moves'
    id = Column(Integer, primary_key=True)
    board_state = Column(String, index=True)
    move = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
