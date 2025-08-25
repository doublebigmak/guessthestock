from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import SessionLocal
from app.models import Game, Price

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/today")
def get_today_games(db: Session = Depends(get_db)):
    today = date.today()
    games = (
        db.query(Game)
        .filter(Game.game_day == today)
        .order_by(Game.game_index)
        .all()
    )

    if len(games) == 0:
        return []

    def to_payload(game):
        prices = (
            db.query(Price)
            .filter(Price.stock_id == game.stock_id, 
                    Price.date >= game.start_date, 
                    Price.date <= game.end_date)
            .order_by(Price.date)
            .all()
        )
        price_data = [{"date": p.date.isoformat(), "close": p.close} for p in prices]
        return {
            "id": game.id,
            "mode": game.mode,
            "prices": price_data,
            "industry": game.stock.industry,
            "ticker": game.stock.ticker,
            "name":game.stock.name,
            "end_year": game.end_date.year
        }

    hard = next((to_payload(g) for g in games if g.mode == "hard"), None)
    easy = next((to_payload(g) for g in games if g.mode == "easy"), None)

    return {'hard':hard,
            "easy":easy}