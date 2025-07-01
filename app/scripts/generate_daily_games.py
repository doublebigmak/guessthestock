
import random
import yfinance as yf
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Game, Price, Stock
from sqlalchemy import func

NUM_GAMES = 3
MIN_DAYS = 90    # ~3 months
MAX_DAYS = 180   # ~6 months

def get_date_range(session: Session, stock_id: int):
    result = (
        session.query(Price.date)
        .filter(Price.stock_id == stock_id)
        .order_by(Price.date)
        .all()
    )
    dates = [r[0] for r in result]
    return dates

def download_prices_for_stock(session: Session, stock: Stock):
    print(f"Fetching data for {stock.ticker}...")
    df = yf.download(stock.ticker, start="2000-01-01", progress=False, auto_adjust=False)
    if df.empty:
        print("No data found.")
        return False

    prices = []
    for dt, row in df.iterrows():
        prices.append(Price(
            stock_id=stock.id,
            date=dt.date(),
            close=row["Close"]
        ))

    session.bulk_save_objects(prices)
    session.commit()
    print(f"{len(prices)} prices inserted for {stock.ticker}.")
    return True


def pick_random_window(dates):
    if len(dates) < MAX_DAYS:
        return None

    max_start_idx = len(dates) - MAX_DAYS
    start_idx = random.randint(0, max_start_idx)
    end_idx = start_idx + random.randint(MIN_DAYS, MAX_DAYS)

    return dates[start_idx], dates[min(end_idx, len(dates)-1)]

def generate_games():
    session = SessionLocal()
    today = date.today()

    stocks = session.query(Stock).order_by(func.random()).all()

    games_created = 0
    index = 0

    for stock in stocks:
        # If prices don't exist yet, download them
        has_prices = session.query(Price).filter(Price.stock_id == stock.id).first()
        if not has_prices:
            if not download_prices_for_stock(session, stock):
                continue  # skip if fetch failed

        dates = get_date_range(session, stock.id)
        window = pick_random_window(dates)
        if not window:
            continue

        start_date, end_date = window

        if len(dates) < MAX_DAYS:
            continue

        window = pick_random_window(dates)
        if not window:
            continue

        start_date, end_date = window

        game = Game(
            stock_id=stock.id,
            start_date=start_date,
            end_date=end_date,
            game_day=today,
            game_index=index
        )
        session.add(game)
        session.commit()

        print(f"✅ Game {index} created for {stock.ticker}: {start_date} to {end_date}")
        games_created += 1
        index += 1

        if games_created == NUM_GAMES:
            break

    if games_created < NUM_GAMES:
        print("⚠️ Not enough stocks with full data to generate 3 games.")

    session.close()

if __name__ == "__main__":
    generate_games()