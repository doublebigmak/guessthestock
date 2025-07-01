from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Float, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    total_score = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    lives_remaining = Column(Integer, default=3)
    last_score = Column(Integer, default=2)
    last_hint_date = Column(Date, nullable=True)

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)

    prices = relationship("Price", back_populates="stock")
    games = relationship("Game", back_populates="stock")



class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint('stock_id', 'date', name='uix_stock_date'),
        Index('idx_price_date', 'date'),
    )

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    date = Column(Date, nullable=False)
    close = Column(Float, nullable=False)

    stock = relationship("Stock", back_populates="prices")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    game_day = Column(Date, nullable=False)  # The day the game is served
    game_index = Column(Integer, nullable=False)  # 0, 1, or 2 (for 3 games per day)

    stock = relationship("Stock", back_populates="games")